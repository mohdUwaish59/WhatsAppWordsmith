from urlextract import URLExtract
from wordcloud import WordCloud
import base64
import plotly.graph_objects as go
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df = df[df['username']==selected_user]

    messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    media=df[df['message'] == '<Media omitted>\n'].shape[0]

    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))
    return messages,len(words),media, len(links)

def fetch_active_users(df):
    users = df['username'].value_counts().head()
    user_stats_df = round((df['username'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'username','value':'percent'})
    return users, user_stats_df

def wordcloud(selected_user, df):
    if selected_user!='Overall':
        df = df[df['username']==selected_user]
    
    f = open('stop_words/stop_words.txt', 'r')
    stop_words=f.read()

    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)

    df_new = df[df['username'] !='Group Notification']
    df_new=df_new[df_new['message'] != '<Media omitted>\n']

    wc=WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_new['message'] = df_new['message'].apply(remove_stop_words)
    df_wc= wc.generate(df_new['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f = open('stop_words/stop_words.txt', 'r')
    stop_words=f.read()

    if selected_user!='Overall':
        df = df[df['username']==selected_user]
    df_new = df[df['username'] !='Group Notification']
    df_new=df_new[df_new['message'] != '<Media omitted>\n']
    words=[]
    for message in df_new['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    df_words = pd.DataFrame(Counter(words).most_common(20))
    df_words.columns = ['words','counts']
    return df_words

def emoji_analysis(selected_user, df):
    if selected_user!='Overall':
        df = df[df['username']==selected_user]
    
    emojis = []
    for message in df['message']:
        emojis.extend([emot for emot in message if emot in emoji.UNICODE_EMOJI['en']])
    df_emoji = pd.DataFrame(Counter(emojis).most_common(len(emojis)))
    print(df_emoji)

    wc=WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_emoji.columns = ['emotess','counts']
    emoji_wc= wc.generate(emoji.demojize(df_emoji['emotess']))

    return df_emoji,emoji_wc

    




    
    
