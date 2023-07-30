import utils

def identify_bullish_harami(tickerData):
    """Identify Bullish Harami patterns."""
    # Calculate the body sizes
    tickerData['Body'] = abs(tickerData['Open'] - tickerData['Close'])

    downtrend = utils.identify_downtrend(tickerData,2,7,.5)

    second_bullish = tickerData['Close'] > tickerData['Open']

    second_engulfed_by_first = (tickerData['Open'] > tickerData['Close'].shift(1)) & \
                           (tickerData['Close'] < tickerData['Open'].shift(1))

    # Bullish Harami pattern
    bullish_harami = downtrend['Downtrend'] & second_bullish & second_engulfed_by_first

    # Add new column for Bullish Harami pattern
    tickerData['Bullish Harami'] = bullish_harami

    return tickerData
