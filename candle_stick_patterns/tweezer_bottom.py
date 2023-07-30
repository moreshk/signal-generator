import utils

def identify_tweezer_bottom(tickerData):
    """Identify Tweezer Bottom patterns."""

    # Check for a downward trend in the past 5 days
    downtrend = utils.identify_downtrend(tickerData,2,7,.2)

    # Check for a bearish candle followed by a bullish candle
    bearish_bullish = (tickerData['Close'].shift(1) < tickerData['Open'].shift(1)) & \
                      (tickerData['Close'] > tickerData['Open'])

    # Check if the second candle opened near to the close of the first candle
    # This can be adjusted depending on the granularity of your data
    same_open_close = abs(tickerData['Open'] - tickerData['Close'].shift(1)) < (tickerData['High'] - tickerData['Low']) * 0.05

    # Combine all the conditions to identify the Tweezer Bottom pattern
    tweezer_bottom = downtrend['Downtrend'] & bearish_bullish & same_open_close

    # Add new column for Tweezer Bottom pattern
    tickerData['Tweezer Bottom'] = tweezer_bottom

    return tickerData
