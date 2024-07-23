import requests
import pandas as pd

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

# Detect sudden price falls and print alerts with dates
def detect_sudden_falls(data, threshold=0.05):
    data['price_change'] = data['close'].pct_change()
    data['sudden_fall'] = data['price_change'] < -threshold

    for date in data[data['sudden_fall']].index:
        print(f"Alert: Price fell suddenly on {date.date()}")

# Main function to execute the process
def main():
    api_key = 'H84F99ZJFXZWJ9UI'
    symbol = input("Enter the stock symbol (e.g., AAPL): ").upper().strip()

    try:
        stock_data = get_stock_data(symbol, api_key)
    except ValueError as e:
        print(e)
        return

    detect_sudden_falls(stock_data)

if __name__ == "__main__":
    main()
