import utils

def identify_bearish_harami(tickerData):
    """Identify Bearish Harami patterns."""
    # Criteria for Bearish Harami pattern
    
    uptrend = utils.identify_uptrend(tickerData,2,4,.3)

    # tickerData['UP'] = uptrend['Uptrend']

    # First candle is bullish
    first_bullish = tickerData['Close'].shift(1) > tickerData['Open'].shift(1)

    # Second candle is bearish
    second_bearish = tickerData['Close'] < tickerData['Open']

    # Second candle body is completely engulfed by First candle body
    second_engulfed_by_first = (tickerData['Open'] < tickerData['Close'].shift(1)) & \
                               (tickerData['Close'] > tickerData['Open'].shift(1))
    
    # All conditions should be met
    bearish_harami = uptrend['Uptrend'] & first_bullish & second_bearish & second_engulfed_by_first

    # Add new column for Bearish Harami pattern
    tickerData['Bearish Harami'] = bearish_harami

    return tickerData
