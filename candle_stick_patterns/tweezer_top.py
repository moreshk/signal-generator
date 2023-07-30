import utils

def identify_tweezer_top(tickerData):
    """Identify Tweezer Top patterns."""

    # Check for an upward trend in the past 5 days
    uptrend = utils.identify_uptrend(tickerData,2,7,.2)

    # Check for a bullish candle followed by a bearish candle
    bullish_bearish = (tickerData['Close'].shift(1) > tickerData['Open'].shift(1)) & \
                      (tickerData['Close'] < tickerData['Open'])

    # Check if the second candle opened near to the close of the first candle
    # This can be adjusted depending on the granularity of your data
    same_open_close = abs(tickerData['Open'] - tickerData['Close'].shift(1)) < (tickerData['High'] - tickerData['Low']) * 0.05

    # Combine all the conditions to identify the Tweezer Top pattern
    tweezer_top = uptrend['Uptrend'] & bullish_bearish & same_open_close

    # Add new column for Tweezer Top pattern
    tickerData['Tweezer Top'] = tweezer_top

    return tickerData
