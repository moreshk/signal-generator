import utils

def identify_inverted_hammer(tickerData):

    downtrend = utils.identify_downtrend(tickerData,1,9,1)
    # Check if body size isn't too small (at least 10% of the candle size)
    tickerData['Body Relative Size'] = tickerData['Body'] / (tickerData['High'] - tickerData['Low'])
    body_size_condition = tickerData['Body Relative Size'] > 0.05

    # Check if the body is in the lower half of the candle - changed from hammer code to identify inverted hammer
    body_location_condition = tickerData['Close'] <= (tickerData['High'] + tickerData['Low']) / 2

    # Check if upper shadow is at least twice the body - changed from hammer code to identify inverted hammer
    upper_shadow_condition = tickerData['Upper Shadow'] >= 2 * tickerData['Body']

    # Check if lower shadow is minimal (no more than 10% of the total candle size) - changed from hammer code to identify inverted hammer
    lower_shadow_condition = tickerData['Lower Shadow'] / (tickerData['High'] - tickerData['Low']) < 0.2

    # Combine all conditions
    tickerData['Inverted Hammer'] = downtrend['Downtrend'] & body_size_condition.astype(bool) & body_location_condition.astype(bool) & upper_shadow_condition.astype(bool) & lower_shadow_condition.astype(bool)

    return tickerData
