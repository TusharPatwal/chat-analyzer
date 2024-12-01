import streamlit as st
import preprocessor
import helper

st.sidebar.title('Whatsapp Chat Analyzer')

upload_file = st.sidebar.file_uploader('Choose a file')
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    st.dataframe(df)

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

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
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