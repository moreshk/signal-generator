from utils import check_trend

def identify_bearish_harami(tickerData):
    """Identify Bearish Harami patterns."""
    # Criteria for Bearish Harami pattern
    
    # check_trend(df, n, trend_type, max_deviation, min_percent_diff):

    uptrend = check_trend(tickerData.shift(2), 4, 'up', 10, 1) 

    # First candle is bullish
    first_bullish = tickerData['Close'].shift(2) > tickerData['Open'].shift(2)

    # Second candle is bullish
    second_bullish = tickerData['Close'].shift(1) > tickerData['Open'].shift(1)

    # Third candle is bearish
    third_bearish = tickerData['Close'] < tickerData['Open']

    # Third candle body is completely engulfed by second candle body
    third_engulfed_by_second = (tickerData['Open'] < tickerData['Close'].shift(1)) & \
                               (tickerData['Close'] > tickerData['Open'].shift(1))
    
    # All conditions should be met
    bearish_harami = uptrend & first_bullish & second_bullish & third_bearish & third_engulfed_by_second
    # bearish_harami = first_bullish & second_bullish & third_bearish & third_engulfed_by_second

    # Add new column for Bearish Harami pattern
    tickerData['Bearish Harami'] = bearish_harami

    return tickerData
