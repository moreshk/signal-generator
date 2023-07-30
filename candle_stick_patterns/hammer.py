import utils

def identify_hammer(tickerData):

    downtrend = utils.identify_downtrend(tickerData,1,9,1)

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
    # tickerData['Hammer'] = tickerData['Trend'].astype(bool) & tickerData['Lower Close'].astype(bool) & tickerData['Lower Open'].astype(bool) & slope_condition.astype(bool) & close_distance_condition.astype(bool) & body_size_condition.astype(bool) & body_location_condition.astype(bool) & shadow_condition.astype(bool) & upper_shadow_condition.astype(bool)
    tickerData['Hammer'] = downtrend['Downtrend'] & body_size_condition.astype(bool) & body_location_condition.astype(bool) & shadow_condition.astype(bool) & upper_shadow_condition.astype(bool)

    return tickerData
