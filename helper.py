from collections import Counter
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = list()
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_msg = df[df['message'].str.contains("<Media omitted>")].shape[0]

    # fetch number of links messages
    links = list()
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_msg, len(links)


def most_busy_user(df):
    x = df[df['users'] != 'group_notification']['users'].value_counts(
    ).reset_index().head()
    bar = px.bar(data_frame=x, x='users', y='count', color='count')

    df = round((df[df['users'] != 'group_notification']['users'].value_counts(
    )/df.shape[0])*100, 2).reset_index().rename(columns={'users': 'name', 'count': 'percent'})
    return bar, df


def create_wordcloud(selected_user, df):
    
    f = open('stop_hinglish.txt', 'r')
    
    stop_words = f.read()
    
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    temp = df[df['users'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('<Media omitted>')]
    temp = temp[~temp['message'].str.contains('<This message was edited>')]

    def remove_stop_words(message):
        y = list()
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
        
    wc = WordCloud(width=700, height=700, min_font_size=10,
                   background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return px.imshow(df_wc)


def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    temp = df[df['users'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('<Media omitted>')]
    temp = temp[~temp['message'].str.contains('<This message was edited>')]

    words = list()

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20), columns=['word', 'count'])
    return px.bar(data_frame=return_df, x=return_df['word'], y=return_df['count'])
    
def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    emojis = list()
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
        
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))), columns=['emoji', 'count'])

    fig = px.pie(data_frame=emoji_df.head(15), names='emoji', values='count')

    return emoji_df, fig

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year','month_num', 'month']).count()['message'].reset_index()
    time = list()
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" +str(timeline['year'][i]))

    timeline['time'] = time
    fig = px.line(data_frame=timeline, x='time', y='message')
    return fig


def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    fig = px.line(data_frame=daily_timeline, x='only_date', y='message')
    
    return fig


def week_acticity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    busy_day = df['day_name'].value_counts().reset_index()
    return px.bar(data_frame=busy_day, x='day_name', y='count', color='day_name')

def month_acticity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    busy_day = df['month'].value_counts().reset_index()
    return px.bar(data_frame=busy_day, x='month', y='count', color='month')


def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    
    new_df = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    fig, ax = plt.subplots()
    ax = sns.heatmap(new_df, cmap='coolwarm')
    # fig = px.imshow(new_df)
    return fig