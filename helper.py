from collections import Counter
import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
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
        
    wc = WordCloud(width=500, height=500, min_font_size=10,
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
    