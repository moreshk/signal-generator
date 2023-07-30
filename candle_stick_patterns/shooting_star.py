import utils

def identify_shooting_star(tickerData):
    """Identify Shooting Star pattern."""
    uptrend = utils.identify_uptrend(tickerData,1,7,.2)

    # uptrend = True

    # Check if body size isn't too small (at least 10% of the candle size)
    tickerData['Body Relative Size'] = tickerData['Body'] / (tickerData['High'] - tickerData['Low'])
    body_size_condition = tickerData['Body Relative Size'] > 0.05

    # Check if the body is in the lower half of the candle
    body_location_condition = tickerData['Close'] <= (tickerData['High'] + tickerData['Low']) / 2

    # Check if upper shadow is at least twice the body
    upper_shadow_condition = tickerData['Upper Shadow'] >= 2 * tickerData['Body']

    # Check if lower shadow is minimal (no more than 10% of the total candle size)
    lower_shadow_condition = tickerData['Lower Shadow'] / (tickerData['High'] - tickerData['Low']) < 0.1

    # Check if the high of the current candle is higher than the high of the previous 2 candles
    higher_high_condition = (tickerData['High'] > tickerData['High'].shift(1)) & (tickerData['High'] > tickerData['High'].shift(2))

    # Combine all conditions
    tickerData['Shooting Star'] =  uptrend['Uptrend'] & body_size_condition.astype(bool) & body_location_condition.astype(bool) & upper_shadow_condition.astype(bool) & lower_shadow_condition.astype(bool) & higher_high_condition.astype(bool)

    return tickerData
