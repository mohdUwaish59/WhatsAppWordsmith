import streamlit as st
import Preprocess_Engine,Telegram_Preprocess_Engine
import Engine
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatspp Chat ANalysis")
file = st.sidebar.file_uploader("Upload chat data file")

if file is not None:
    if file.type == "text/plain":
        bytesdata = file.getvalue()
        data= bytesdata.decode("utf-8")
        df=Preprocess_Engine.data_Preprocess(data)
    elif file.type == "text/html":
        bytesdata = file.getvalue()
        data= bytesdata.decode("utf-8")
        df=Telegram_Preprocess_Engine.data_Preprocess(data)



    st.dataframe(df)
    users = df['username'].unique().tolist()
    users.remove('Group Notification')
    users.sort()
    users.insert(0, 'Overall')

    selected_user=st.sidebar.selectbox("Analysis of", users)

    if st.sidebar.button("Analyze"):
        messages, words, media, links =  Engine.fetch_stats(selected_user,df)
        col1, col2, col3, col4 =st.columns(4)

        with col1:
            st.header("Total Messages:")
            st.title(messages)
        with col2:
            st.header("Total words:")
            st.title(words)
        with col3:
            st.header("Total Media Files:")
            st.title(media)
        with col4:
            st.header("Total Links Shared:")
            st.title(links)
        image1 = Engine.wordcloud(selected_user, df)
        st.header('Most frequent words')
        st.image(image1.to_array())
        
        if selected_user=='Overall':
            st.title("Most Active Users")
            users, user_stats_df = Engine.fetch_active_users(df)
            fig = px.bar(df, x= users.index, y=users.values, title='',width=300, height=400)
            fig.update_xaxes(tickangle=90)

            col1, col2=st.columns(2)

            with col1:
                st.plotly_chart(fig)
            with col2:
                st.dataframe(user_stats_df)
        
        words_df = Engine.most_common_words(selected_user,df)
        fig_words = px.bar(words_df, y= words_df.words, x=words_df.counts, title='',width=500, height=500)
        st.header("Most Frequent words")
        st.plotly_chart(fig_words)
        #st.dataframe(words_df)
        df_emoji ,emoji_wc= Engine.emoji_analysis(selected_user, df)
        col1, col2 =st.columns(2)

        with col1:
            st.header('Most frequent emojis')
            st.image(emoji_wc.to_array())

        fig3 = px.pie(df_emoji,names=df_emoji.emotess, values=df_emoji.counts, title='Emoji Usage Distribution')

        with col2:
            st.header('Most frequent emojis')
            st.plotly_chart(fig3)

        
        monthly_data, monthly_data_count = Engine.monthly_data(selected_user, df)
        fig_m = px.line(monthly_data, y= monthly_data.message, x = monthly_data.timeline)
        fig_b = px.bar(monthly_data_count, x=monthly_data_count.index,y=monthly_data_count.values)
        st.header("Monthly Activity")
        st.plotly_chart(fig_m)
        st.plotly_chart(fig_b)


        daily_data = Engine.daily_data(selected_user, df)
        print(daily_data)
        fig_d = px.line(daily_data, y= daily_data.message, x = daily_data.only_date)
        st.plotly_chart(fig_d)

        st.title("Weekly Activity")
        col1, col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day = Engine.week_data(selected_user,df)
            fig = px.bar(busy_day,x=busy_day.index, y= busy_day.values)
            st.plotly_chart(fig)



        heatmap  = Engine.activity_heat_map(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(heatmap)
        
        st.pyplot(fig)





            

        
