import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from transformers import pipeline
import requests

# Your News API key
news_api_key = '18e008e7cf6d43cc9c826b2d991ddb8f'

# Function to fetch commodity data
def fetch_commodity_data(ticker):
    data = yf.download(ticker, period="1y")
    return data

# Function to calculate moving averages
def calculate_moving_average(data, window=5):
    data['MA'] = data['Close'].rolling(window=window).mean()
    return data

# Function to fetch news and perform sentiment analysis using transformers
def fetch_news_sentiment(query):
    news_url = f"https://newsapi.org/v2/everything?q={query}&apiKey={news_api_key}"
    response = requests.get(news_url)
    news_data = response.json()

    if 'articles' in news_data:
        articles = news_data['articles']
        nlp = pipeline('sentiment-analysis')
        sentiments = [nlp(article['title'])[0]['score'] * (1 if nlp(article['title'])[0]['label'] == 'POSITIVE' else -1) for article in articles]
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        return avg_sentiment
    else:
        return 0

# Determine buy/sell signals
def determine_trade_signal(data, sentiment):
    recent_price = data['Close'].iloc[-1]
    moving_avg = data['MA'].iloc[-1]

    if recent_price < moving_avg and sentiment > 0.1:
        return "BUY"
    elif recent_price > moving_avg and sentiment < -0.1:
        return "SELL"
    else:
        return "HOLD"

# Streamlit app
st.title("Commodity Trade Signals")
st.markdown("## Gold and Silver Trading Recommendations Based on Moving Averages and News Sentiment")

# Fetch and display gold data
st.markdown("### Gold Data")
gold_data = fetch_commodity_data('GC=F')
gold_data = calculate_moving_average(gold_data)
st.line_chart(gold_data['Close'], use_container_width=True)
st.line_chart(gold_data['MA'], use_container_width=True)

# Fetch and display silver data
st.markdown("### Silver Data")
silver_data = fetch_commodity_data('SI=F')
silver_data = calculate_moving_average(silver_data)
st.line_chart(silver_data['Close'], use_container_width=True)
st.line_chart(silver_data['MA'], use_container_width=True)

# Fetch news sentiment and determine trade signals
gold_sentiment = fetch_news_sentiment('gold')
silver_sentiment = fetch_news_sentiment('silver')
gold_signal = determine_trade_signal(gold_data, gold_sentiment)
silver_signal = determine_trade_signal(silver_data, silver_sentiment)

# Display trade signals
st.markdown(f"### Gold Trade Signal: **{gold_signal}**")
st.markdown(f"### Silver Trade Signal: **{silver_signal}**")
