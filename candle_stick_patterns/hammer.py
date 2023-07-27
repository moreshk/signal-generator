import utils

def identify_hammer(tickerData):
    """Identify Hammer pattern."""
    # Calculate previous trend (True if decreasing over last 12 days)
    tickerData['Trend'] = tickerData['Close'].rolling(window=13).apply(lambda x: x[0] > x[-1])

    # Check if current candle's close is lower than all previous 12 candles
    tickerData['Lower Close'] = True
    # tickerData['Close'].rolling(window=13).apply(lambda x: x[-1] < min(x[:-1]))

    # Check if current candle's open is lower than all previous 12 candles
    tickerData['Lower Open'] = tickerData['Open'].rolling(window=13).apply(lambda x: x[-1] < min(x[:-1]))

    # Calculate slope of line between the first and the last candle in window, then ensure it's negative
    tickerData['Slope'] = tickerData['Close'].rolling(window=13).apply(lambda x: (x[-1] - x[0])/12)
    slope_condition = tickerData['Slope'] < 0

    # Check that close of all interim candles is not too far from the line
    tickerData['Close Distance'] = tickerData['Close'].rolling(window=13).apply(utils.calculate_distance)
    close_distance_condition = tickerData['Close Distance'] <= 0.011

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
    tickerData['Hammer'] = tickerData['Trend'].astype(bool) & tickerData['Lower Close'].astype(bool) & tickerData['Lower Open'].astype(bool) & slope_condition.astype(bool) & close_distance_condition.astype(bool) & body_size_condition.astype(bool) & body_location_condition.astype(bool) & shadow_condition.astype(bool) & upper_shadow_condition.astype(bool)

    return tickerData
