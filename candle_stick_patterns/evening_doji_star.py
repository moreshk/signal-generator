import utils

def identify_evening_doji_star(tickerData):
    """Identify Evening Doji Star pattern."""
    tickerData = utils.calculate_body_and_doji(tickerData)
    
    # Calculate Small Doji condition for the second candle
    shifted_tickerData = tickerData.shift(1)
    utils.calculate_smalldoji(shifted_tickerData)

    uptrend = utils.identify_uptrend(tickerData,3,3,.1)
    
    first_candle_bullish = tickerData['Close'].shift(2) > tickerData['Open'].shift(2)
    first_candle_not_doji = ~(tickerData['Doji'].shift(2).fillna(False).astype(bool))   # First candle is not a doji
    second_candle_doji = shifted_tickerData['Small Doji']
    gap_up_first_second = tickerData['Open'].shift(1) > tickerData['Close'].shift(2)
    third_candle_bearish = tickerData['Open'] > tickerData['Close']
    third_candle_not_doji = ~(tickerData['Doji'].fillna(False).astype(bool))   # Third candle is not a doji
    gap_down_second_third = tickerData['Open'] < tickerData['Close'].shift(1)

    tickerData['Evening Doji Star'] = uptrend['Uptrend'] & first_candle_bullish & first_candle_not_doji & second_candle_doji & gap_up_first_second & third_candle_bearish & third_candle_not_doji & gap_down_second_third
    
    return tickerData
