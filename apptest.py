import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

# Sample data
text = "Hello Streamlit is a great tool for creating web apps with Python. Streamlit is easy to use and powerful. You can create data visualizations using Plotly in Streamlit."

# Create a word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Create a Plotly bar chart of word frequency
word_freq = pd.Series(text.split()).value_counts()
word_freq_df = pd.DataFrame({'Word': word_freq.index, 'Frequency': word_freq.values})
fig = px.bar(word_freq_df, x='Word', y='Frequency', title='Word Frequency')
fig.update_xaxes(tickangle=45)

# Streamlit app
st.title("Word Cloud and Word Frequency Analysis")
st.sidebar.header("Word Cloud Settings")
st.image(wordcloud.to_array())

# Display word frequency chart
st.plotly_chart(fig)

# Display the raw text
st.sidebar.subheader("Raw Text")
st.sidebar.text(text)

# Streamlit app footer
st.sidebar.text("Created by Your Name")

