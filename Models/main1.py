import requests
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Function to get stock data from Alpha Vantage
def get_stock_data(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}&outputsize=full'
    response = requests.get(url)
    data = response.json()

    if "Time Series (Daily)" not in data:
        raise ValueError(f"Error fetching data for {symbol}: {data}")

    df = pd.DataFrame(data["Time Series (Daily)"]).T
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    df.sort_index(inplace=True)

    return df


# Detect sudden price changes
def detect_sudden_changes(data, threshold=0.05):
    data['price_change'] = data['close'].pct_change()
    data['sudden_fall'] = data['price_change'] < -threshold
    data['sudden_rise'] = data['price_change'] > threshold
    return data


# Feature engineering
def add_features(data):
    data['7d_avg'] = data['close'].rolling(window=7).mean()
    data['30d_avg'] = data['close'].rolling(window=30).mean()
    data['365d_avg'] = data['close'].rolling(window=365).mean()
    data['7d_std'] = data['close'].rolling(window=7).std()
    data['30d_std'] = data['close'].rolling(window=30).std()
    return data.dropna()


# Prepare data for training
def prepare_training_data(data):
    data = add_features(data)
    X = data[['7d_avg', '30d_avg', '365d_avg', '7d_std', '30d_std']]
    y = np.where(data['close'].shift(-30 * 6) > data['close'], 1, 0)  # Long term: 6 months (approx. 180 days)
    y_short = np.where(data['close'].shift(-30) > data['close'], 1, 0)  # Short term: 1 month (approx. 30 days)
    return X, y, y_short


# Train models
def train_models(X, y, y_short):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train_short, X_test_short, y_train_short, y_test_short = train_test_split(X, y_short, test_size=0.2,
                                                                                random_state=42)

    clf_long = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_short = RandomForestClassifier(n_estimators=100, random_state=42)

    clf_long.fit(X_train, y_train)
    clf_short.fit(X_train_short, y_train_short)

    y_pred = clf_long.predict(X_test)
    y_pred_short = clf_short.predict(X_test_short)

    print("Long-term accuracy:", accuracy_score(y_test, y_pred))
    print("Short-term accuracy:", accuracy_score(y_test_short, y_pred_short))

    return clf_long, clf_short


# Function to predict and provide alerts
def predict_and_alert(data, clf_long, clf_short):
    data = add_features(data)
    X = data[['7d_avg', '30d_avg', '365d_avg', '7d_std', '30d_std']]

    data['long_term_signal'] = clf_long.predict(X)
    data['short_term_signal'] = clf_short.predict(X)

    alerts = data[(data['sudden_fall'] | data['sudden_rise'])]
    recommendations = data[(data['long_term_signal'] == 1) | (data['short_term_signal'] == 1)]

    return alerts, recommendations


# Function to calculate the number of shares and profit
def calculate_investment_recommendations(recommendations, investment_amount):
    current_price = recommendations['close'][-1]
    shares_to_buy = investment_amount // current_price
    investment_value = shares_to_buy * current_price

    # Estimate profits after 6 months and 1 year
    future_price_6m = recommendations['close'].shift(-180).iloc[-1]  # Approx 6 months
    future_price_1y = recommendations['close'].shift(-365).iloc[-1]  # Approx 1 year

    profit_6m = shares_to_buy * (future_price_6m - current_price)
    profit_1y = shares_to_buy * (future_price_1y - current_price)

    return shares_to_buy, profit_6m, profit_1y


# Main function to execute the process
def main():
    api_key = 'H84F99ZJFXZWJ9UI'
    symbol = 'AAPL'
    investment_amount = 10000  # Example investment amount

    stock_data = get_stock_data(symbol, api_key)
    stock_data = detect_sudden_changes(stock_data)

    X, y, y_short = prepare_training_data(stock_data)
    clf_long, clf_short = train_models(X, y, y_short)

    alerts, recommendations = predict_and_alert(stock_data, clf_long, clf_short)
    print("Alerts:\n", alerts[['close', 'sudden_fall', 'sudden_rise']])

    # Print recommendations for long-term and short-term
    long_term_recommendations = recommendations[recommendations['long_term_signal'] == 1]
    short_term_recommendations = recommendations[recommendations['short_term_signal'] == 1]
    print("Long-term Recommendations:\n", long_term_recommendations[['close']])
    print("Short-term Recommendations:\n", short_term_recommendations[['close']])

    # Calculate investment recommendations
    shares_to_buy, profit_6m, profit_1y = calculate_investment_recommendations(long_term_recommendations,
                                                                               investment_amount)
    print(f"With an investment of ${investment_amount}, you should buy {shares_to_buy} shares.")
    print(f"Estimated profit after 6 months: ${profit_6m:.2f}")
    print(f"Estimated profit after 1 year: ${profit_1y:.2f}")


if __name__ == "__main__":
    main()

