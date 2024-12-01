import streamlit as st
import preprocessor

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
    
    st.sidebar.selectbox('Show Analisis on', user_list)
    
    if st.sidebar.button('Show Analysis'):
        pass