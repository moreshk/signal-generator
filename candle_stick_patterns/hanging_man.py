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

def identify_hanging_man(tickerData):
    """Identify Hanging Man pattern."""
    # Calculate previous trend (True if increasing over last 12 days)
    tickerData['Trend'] = tickerData['Close'].rolling(window=13).apply(lambda x: x[0] < x[-1])

    # Check if current candle's close is higher than all previous 12 candles
    tickerData['Higher Close'] = tickerData['Close'].rolling(window=13).apply(lambda x: x[-1] > max(x[:-1]))

    # Calculate slope of line between the first and the last candle in window, then ensure it's positive
    tickerData['Slope'] = tickerData['Close'].rolling(window=13).apply(lambda x: (x[-1] - x[0])/12)
    slope_condition = tickerData['Slope'] > 0

    # Check that close of all interim candles is not too far from the line
    tickerData['Close Distance'] = tickerData['Close'].rolling(window=13).apply(calculate_distance)
    close_distance_condition = tickerData['Close Distance'] <= 0.01

    # Check if body size isn't too small (at least 10% of the candle size)
    tickerData['Body Relative Size'] = tickerData['Body'] / (tickerData['High'] - tickerData['Low'])
    body_size_condition = tickerData['Body Relative Size'] > 0.05

    # Check if the body is in the upper half of the candle  
    body_location_condition = tickerData['Close'] > (tickerData['High'] + tickerData['Low']) / 2

    # Check if lower shadow is at least twice the body
    shadow_condition = tickerData['Lower Shadow'] >= 2 * tickerData['Body']

    # Check if upper shadow is minimal (no more than 10% of the total candle size)
    upper_shadow_condition = tickerData['Upper Shadow'] / (tickerData['High'] - tickerData['Low']) < 0.2

    # Combine all conditions
    tickerData['Hanging Man'] = tickerData['Trend'].astype(bool) & tickerData['Higher Close'].astype(bool) & slope_condition.astype(bool) & close_distance_condition.astype(bool) & body_size_condition.astype(bool) & body_location_condition.astype(bool) & shadow_condition.astype(bool) & upper_shadow_condition.astype(bool)

    return tickerData
