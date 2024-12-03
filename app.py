import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.title('Whatsapp Chat Analyzer')

upload_file = st.sidebar.file_uploader('Choose a file')
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Show Analisis on', user_list)

    if st.sidebar.button('Show Analysis'):

        # Stats Area
        num_messages, words, num_media_msg, link_shared = helper.fetch_stats(
            selected_user, df)
        st.title('Top Statistics')
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Msgs')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(words)

        with col3:
            st.header('Media Shared')
            st.title(num_media_msg)

        with col4:
            st.header('Links Shared')
            st.title(link_shared)
            
    # monthly timeline
    st.title('Monthly Timeline')
    timeline = helper.monthly_timeline(selected_user, df)
    st.plotly_chart(timeline)
    
    # daily timeline
    st.title('Daily Timeline')
    d_timeline = helper.daily_timeline(selected_user, df)
    st.plotly_chart(d_timeline)

    # activity map 
    st.title('Activity Map')
    col1, col2 = st.columns(2)

    with col1:
        st.header('Most busy day')
        busy_day = helper.week_acticity_map(selected_user, df)
        st.plotly_chart(busy_day)
    
    with col2:
        st.header('Most busy month')
        busy_month = helper.month_acticity_map(selected_user, df)
        st.plotly_chart(busy_month)

    user_heatmap = helper.activity_heatmap(selected_user, df)
    
    st.title('Weekly Activity Map')
    st.pyplot(user_heatmap)
    # st.plotly_chart(user_heatmap)

    # finding the busiest users in the group(group level)
    if selected_user == 'Overall':
        st.title('Most Busy User')
        col1, col2 = st.columns(2)
        x, new_df = helper.most_busy_user(df)
        
        with col1:
            st.plotly_chart(x)
        
        with col2:
            st.dataframe(new_df)
            
    # create wordcloud
    st.title('WordCloud')
    df_wc = helper.create_wordcloud(selected_user, df)
    st.plotly_chart(df_wc)
    
    # most common words
    st.title('Most common words')
    most_common_words = helper.most_common_words(selected_user, df)

    st.plotly_chart(most_common_words)
    
    # emoji analysis
    emoji_df, fig = helper.emoji_helper(selected_user, df)
    st.title('Emoji Analysis')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(emoji_df)

    with col2:
        st.plotly_chart(fig)
        
    