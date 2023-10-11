import re
import pandas as pd
import csv
from bs4 import BeautifulSoup

def data_Preprocess(data):
    # Create a BeautifulSoup object
        soup = BeautifulSoup(data, 'html.parser')

        # Find all message containers
        message_containers = soup.find_all('div', class_='message default clearfix')

        # Initialize lists to store extracted data
        usernames = []
        timestamps = []
        message_contents = []

        for message_div in message_containers:
            # Extract message content, username, and timestamp for each message
            text_div = message_div.find('div', class_='text')
            username_div = message_div.find('div', class_='from_name')
            timestamp_div = message_div.find('div', class_='pull_right date details')
            if text_div:
                message_content = text_div.get_text(strip=True)
            else:
                message_content = "Message content not found"

            if username_div:
                username = username_div.get_text()
            else:
                username = "Username not found"

            if timestamp_div:
                timestamp = timestamp_div['title']
            else:
                timestamp = "Timestamp not found"

            # Append the extracted data to the lists
            usernames.append(username)
            timestamps.append(timestamp)
            message_contents.append(message_content)

        # Create a pandas DataFrame for Telegram chat data
        df = pd.DataFrame({
            'username': usernames,
            'date': timestamps,
            'message': message_contents
        })

        df['date'] = pd.to_datetime(df['date'])
        df['username'] = df['username'].str.split('\n').str[1]
        df['only_date'] = df['date'].dt.date
        df['year'] = df['only_date'].apply(lambda x: x.year)
        df['month_num'] = df['only_date'].apply(lambda x: x.month)
        df['day'] = df['only_date'].apply(lambda x: x.day)
        df['month'] = df['only_date'].apply(lambda x: x.strftime('%B'))
        df['day_name'] = df['only_date'].apply(lambda x: x.strftime('%A'))
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        period = []
        for hour in df[['day_name', 'hour']]['hour']:
            if hour == 23:
                period.append(str(hour) + "-" + str('00'))
            elif hour == 0:
                period.append(str('00') + "-" + str(hour + 1))
            else:
                period.append(str(hour) + "-" + str(hour + 1))
        df['period'] = period

        custom_data = {'username':'Group Notification',
                        'date':'2022-02-16 14:48:07-01:00', 
                        'message':'a', 
                        'only_date':'2022-02-16', 
                        'year':'2022', 
                        'month_num':'02', 
                        'day':'16',
                        'month_name':'February', 
                        'day_name':'Wednesday', 
                        'hour':'14', 
                        'minute':'48', 
                        'period':'14-15'}

        custom_row = pd.DataFrame([custom_data])
        df = pd.concat([df, custom_row], ignore_index=True)


        return df