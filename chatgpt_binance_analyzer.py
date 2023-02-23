# pip install python-binance numpy

from binance.client import Client
import numpy as np

# Replace YOUR_API_KEY and YOUR_SECRET_KEY with your own keys
api_key = "YOUR_API_KEY"  # Можно удалить
api_secret = "YOUR_SECRET_KEY"  # Можно удалить

# Initialize the client with your API key and secret
client = Client(api_key, api_secret)   # api_key и api_secret можно не передавать в качестве аргументов

# Get the ticker prices for all trading pairs
tickers = client.get_all_tickers()

# Loop through all trading pairs
for ticker in tickers:
    symbol = ticker['symbol']
    if symbol[-4:] == 'USDT':
        # Get the klines data for the past 24 hours
        klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "24 hours ago UTC")

        # Extract the closing prices
        closing_prices = np.array([float(kline[4]) for kline in klines])

        if len(closing_prices) >= 20:
            # Compute the simple moving averages
            sma5 = np.convolve(closing_prices, np.ones(5) / 5, mode='valid')
            sma20 = np.convolve(closing_prices, np.ones(20) / 20, mode='valid')
            sma20_adjusted = np.pad(sma20, (len(sma5) - len(sma20), 0), 'constant')

            # Compute the crossover signal
            signal = np.where(sma5 > sma20_adjusted, 1, -1)

            # Determine the position (buy/sell/hold)
            if signal[-1] > signal[-2]:
                position = "Buy"
            elif signal[-1] < signal[-2]:
                position = "Sell"
            else:
                position = "Hold"

            # Print the trading pair and position
            print(symbol, position)
