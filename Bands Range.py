!pip install pandas ta requests

import pandas as pd
import ta
import requests
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator

# Fetch data from Token Metrics API
api_key = "tm-********-****-****-****-************"
token_id = "3375"  # Replace this with the SHIB token ID from Token Metrics
start_date = "2021-01-01"
end_date = "2021-12-31"

ohlcv_url = f"https://api.tokenmetrics.com/v1/tokens/{token_id}/ohlcv?start_date={start_date}&end_date={end_date}"

headers = {
    "accept": "application/json",
    "api_key": api_key
}

response = requests.get(ohlcv_url, headers=headers)
print(response.text)  # Add this line to print the response content
ohlcv_data = response.json()['data']


# Create a DataFrame
df = pd.DataFrame(ohlcv_data)
df['date'] = pd.to_datetime(df['date'])
df['price'] = df['close'].astype(float)

# Calculate Bollinger Bands
bb = BollingerBands(df['price'], window=20, window_dev=2)
df['bb_high'] = bb.bollinger_hband()
df['bb_low'] = bb.bollinger_lband()

# Calculate RSI
rsi = RSIIndicator(df['price'], window=14)
df['rsi'] = rsi.rsi()

# Define entry signals
def signal(row):
    if row['price'] < row['bb_low'] and row['rsi'] < 30:
        return 'Buy'
    elif row['price'] > row['bb_high'] and row['rsi'] > 70:
        return 'Sell'
    else:
        return 'Hold'

df['signal'] = df.apply(signal, axis=1)

# Print the resulting DataFrame
print(df)
