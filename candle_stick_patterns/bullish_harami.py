from utils import check_trend

def identify_bullish_harami(tickerData):
    """Identify Bullish Harami patterns."""
    # Calculate the body sizes
    tickerData['Body'] = abs(tickerData['Open'] - tickerData['Close'])

    # Criteria for Bullish Harami pattern
    # first_two_bearish = (tickerData['Close'].shift(2) < tickerData['Open'].shift(2)) & \
                        # (tickerData['Close'].shift(1) < tickerData['Open'].shift(1))
    
    # check_trend(df, n, trend_type, max_deviation, min_percent_diff):

    downtrend = check_trend(tickerData.shift(2), 4, 'down', 10, 1)  # Shift the data by 2 periods


    third_bullish = tickerData['Close'] > tickerData['Open']

    third_engulfed_by_second = (tickerData['Open'] > tickerData['Close'].shift(1)) & \
                           (tickerData['Close'] < tickerData['Open'].shift(1))

    # Bullish Harami pattern
    bullish_harami = downtrend & third_bullish & third_engulfed_by_second

    # Add new column for Bullish Harami pattern
    tickerData['Bullish Harami'] = bullish_harami

    return tickerData
