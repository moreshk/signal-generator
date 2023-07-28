import numpy as np
import pandas as pd

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

def calculate_body_and_doji(tickerData):
    """Calculate the body size and identify dojis."""
    tickerData['Body'] = abs(tickerData['Open'] - tickerData['Close'])
    tickerData['Doji'] = (tickerData['Body'] / (tickerData['High'] - tickerData['Low'])) < 0.2
    return tickerData


def check_trend(df, n, trend_type, max_deviation, min_percent_diff):
    df = df[-n:]  # Take the last n rows

    if trend_type.lower() == 'up':
        # Calculate the percent difference between the first open and last close
        percent_diff = (df['Close'].iat[-1] - df['Open'].iat[0]) / df['Open'].iat[0] * 100
    elif trend_type.lower() == 'down':
        # Calculate the percent difference between the first open and last close
        percent_diff = (df['Open'].iat[0] - df['Close'].iat[-1]) / df['Open'].iat[0] * 100


    # Create the x coordinates [0, 1, 2, ..., n-1]
    x_coords = np.arange(n)
    # Get the y coordinates (the mid point between the open and close prices)
    y_coords = (df['Open'] + df['Close']) / 2

    # Fit a line to the points
    slope, intercept = np.polyfit(x_coords, y_coords, 1)

    # Check if slope matches the trend type
    # if (trend_type.lower() == 'up' and slope < 0) or (trend_type.lower() == 'down' and slope > 0):
    #     return False
    
    # Calculate the distance from each point to the line
    distances = abs(slope * x_coords + intercept - y_coords) / np.sqrt(slope**2 + 1)
    # Get the maximum deviation
    max_distance = distances.max()

    # Calculate the percent deviation
    percent_deviation = max_distance / df['Close'].mean() * 100

    return percent_deviation <= max_deviation
