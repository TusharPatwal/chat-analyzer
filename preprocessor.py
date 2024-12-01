import pandas as pd
import re

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # converting data into dataframe
    df = pd.DataFrame({'user_message':message, 'message_date':dates})

    # convert messages_date type
    df['message_date'] = df['message_date'].str.replace(' - ','')
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %H:%M")
    
    # rename the column
    df.rename(columns={'message_date':'date'}, inplace=True)
    
    # seperate users and messages
    users = list()
    messages = list()

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    
    # extracting date & time from date column
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['only_date'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    return df