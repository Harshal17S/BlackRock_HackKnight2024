import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import requests
from transformers import pipeline


# Function to get current market data
def get_market_data(symbol):
    api_key = 'H84F99ZJFXZWJ9UI'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    if "Time Series (Daily)" in data:
        return data["Time Series (Daily)"]
    else:
        st.error("Error fetching market data. Please check the symbol and API key.")
        return None


# Function to get financial news
def get_financial_news():
    api_key = '18e008e7cf6d43cc9c826b2d991ddb8f'
    url = f'https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={api_key}'
    response = requests.get(url)
    news_data = response.json()
    if news_data["status"] == "ok":
        return news_data["articles"]
    else:
        st.error("Error fetching news data. Please check the API key.")
        return None


# Define the calculation function with exception handling
def calculate_retirement_savings(current_age, retirement_age, current_savings, annual_contribution, return_rate,
                                 has_disease):
    try:
        years_to_retirement = retirement_age - current_age
        if years_to_retirement <= 0:
            raise ValueError("Retirement age must be greater than current age.")

        if has_disease:
            return_rate -= 0.01  # Reduce the return rate by 1% if the user has a disease

        future_value = current_savings
        savings_over_time = [current_savings]

        for _ in range(years_to_retirement):
            future_value += annual_contribution
            future_value *= (1 + return_rate)
            savings_over_time.append(future_value)

        return future_value, savings_over_time

    except ValueError as e:
        st.error(f"Value Error: {e}")
        return None, None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None, None


# Define the investment suggestion function with sentiment analysis
def suggest_investments(return_rate, market_data, news_data):
    sentiment_analyzer = pipeline("sentiment-analysis")

    if return_rate <= 0.03:
        suggestion = "Consider low-risk investments such as bonds or savings accounts."
    elif return_rate <= 0.07:
        suggestion = "Consider a balanced portfolio with a mix of stocks and bonds."
    else:
        suggestion = "Consider higher-risk investments such as stocks, mutual funds, or real estate."

    # Adding market data and news analysis
    if market_data and news_data:
        latest_news = news_data[0]["title"]
        sentiment = sentiment_analyzer(latest_news)[0]
        if sentiment["label"] == "POSITIVE":
            suggestion += f" Based on the latest news: '{latest_news}', which is positive, you might want to look into the current market trends."
        else:
            suggestion += f" Based on the latest news: '{latest_news}', which is negative, you might want to be cautious about the current market trends."

    return suggestion


# Streamlit UI
st.title('Retirement Planning Calculator')

# Input fields
current_age = st.number_input('Current Age:', min_value=0, max_value=100, value=30)
retirement_age = st.number_input('Retirement Age:', min_value=current_age, max_value=100, value=65)
current_savings = st.number_input('Current Savings ($):', min_value=0, value=10000)
annual_contribution = st.number_input('Annual Contribution ($):', min_value=0, value=5000)
return_rate = st.number_input('Expected Annual Return Rate (as a decimal):', min_value=0.0, max_value=1.0, value=0.05)

# New input field for health consideration
has_disease = st.checkbox('Do you have any existing diseases that may affect your savings?')

# Calculate button
if st.button('Calculate'):
    future_savings, savings_over_time = calculate_retirement_savings(current_age, retirement_age, current_savings,
                                                                     annual_contribution, return_rate, has_disease)

    if future_savings is not None:
        st.write(f'Estimated Retirement Savings: ${future_savings:,.2f}')

        # Fetch market data and news
        market_data = get_market_data('AAPL')  # Example with Apple stock symbol
        news_data = get_financial_news()

        # Provide investment suggestions
        investment_suggestion = suggest_investments(return_rate, market_data, news_data)
        st.write(f'Investment Suggestion: {investment_suggestion}')

        # Plot savings over time
        years = list(range(current_age, retirement_age + 1))
        plt.figure(figsize=(10, 6))
        plt.plot(years, savings_over_time, marker='o', linestyle='-', color='b')
        plt.title('Retirement Savings Growth Over Time')
        plt.xlabel('Age')
        plt.ylabel('Savings ($)')
        plt.grid(True)
        plt.xticks(np.arange(current_age, retirement_age + 1, step=max((retirement_age - current_age) // 10, 1)))
        plt.yticks(np.arange(0, max(savings_over_time) + 1, step=max(int(max(savings_over_time) // 10), 10000)))
        st.pyplot(plt)
    else:
        st.write('Unable to calculate retirement savings due to input error.')

# Note: Run this application by entering "streamlit run retirement_savings_calculator.py" in the terminal window.
