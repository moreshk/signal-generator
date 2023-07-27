import numpy as np

def calculate_body_and_shadow(tickerData):
    """Calculate the body size and the upper and lower shadow sizes."""
    tickerData['Body'] = abs(tickerData['Open'] - tickerData['Close'])
    tickerData['Lower Shadow'] = tickerData[['Open', 'Close']].min(axis=1) - tickerData['Low']
    tickerData['Upper Shadow'] = tickerData['High'] - tickerData[['Open', 'Close']].max(axis=1)
    return tickerData


def calculate_distance(x):
    """Calculate maximum absolute percentage difference between actual and predicted closing prices."""
    a, b = np.polyfit(np.arange(len(x)), x, 1)
    y = a * np.arange(len(x)) + b
    return max(abs((x - y) / x))