import utils

def identify_shooting_star(tickerData):
    """Identify Shooting Star pattern."""
    # Calculate previous trend (True if increasing over last 5 days)
    tickerData['Trend'] = tickerData['Close'].rolling(window=6).apply(lambda x: x[0] < x[-1])

    # Check if current candle's close is higher than all previous 5 candles
    tickerData['Higher Close'] = tickerData['Close'].rolling(window=6).apply(lambda x: x[-1] > max(x[:-1]))

    # Check if current candle's open is higher than all previous 5 candles
    tickerData['Higher Open'] = True

    # tickerData['Open'].rolling(window=6).apply(lambda x: x[-1] > max(x[:-1]))

    # Calculate slope of line between the first and the last candle in window, then ensure it's positive
    tickerData['Slope'] = tickerData['Close'].rolling(window=6).apply(lambda x: (x[-1] - x[0])/5)
    slope_condition = tickerData['Slope'] > 0

    # Check that close of all interim candles is not too far from the line
    tickerData['Close Distance'] = tickerData['Close'].rolling(window=6).apply(utils.calculate_distance)
    close_distance_condition = tickerData['Close Distance'] <= 0.011

    # Check if body size isn't too small (at least 10% of the candle size)
    tickerData['Body Relative Size'] = tickerData['Body'] / (tickerData['High'] - tickerData['Low'])
    body_size_condition = tickerData['Body Relative Size'] > 0.05

    # Check if the body is in the lower half of the candle
    body_location_condition = tickerData['Close'] <= (tickerData['High'] + tickerData['Low']) / 2

    # Check if upper shadow is at least twice the body
    upper_shadow_condition = tickerData['Upper Shadow'] >= 2 * tickerData['Body']

    # Check if lower shadow is minimal (no more than 10% of the total candle size)
    lower_shadow_condition = tickerData['Lower Shadow'] / (tickerData['High'] - tickerData['Low']) < 0.1

    # Combine all conditions
    tickerData['Shooting Star'] = tickerData['Trend'].astype(bool) & tickerData['Higher Close'].astype(bool) & tickerData['Higher Open'].astype(bool) & slope_condition.astype(bool) & close_distance_condition.astype(bool) & body_size_condition.astype(bool) & body_location_condition.astype(bool) & upper_shadow_condition.astype(bool) & lower_shadow_condition.astype(bool)

    return tickerData
