import utils

def identify_morning_doji_star(tickerData):
    """Identify Morning Doji Star pattern."""
    tickerData = utils.calculate_body_and_doji(tickerData)
    
    # Calculate Small Doji condition for the second candle
    shifted_tickerData = tickerData.shift(1)
    utils.calculate_smalldoji(shifted_tickerData)

    downtrend = utils.identify_downtrend(tickerData,3,3,.1)
    
    first_candle_bearish = tickerData['Open'].shift(2) > tickerData['Close'].shift(2)
    first_candle_not_doji = ~(tickerData['Doji'].shift(2).fillna(False).astype(bool))   # First candle is not a doji
    second_candle_doji = shifted_tickerData['Small Doji']
    gap_down_first_second = tickerData['Close'].shift(2) > tickerData['Open'].shift(1)
    third_candle_bullish = tickerData['Close'] > tickerData['Open']
    third_candle_not_doji = ~(tickerData['Doji'].fillna(False).astype(bool))   # Third candle is not a doji
    gap_up_second_third = tickerData['Close'].shift(1) < tickerData['Open']

    tickerData['Morning Doji Star'] = downtrend['Downtrend'] & first_candle_bearish & first_candle_not_doji & second_candle_doji & gap_down_first_second & third_candle_bullish & third_candle_not_doji & gap_up_second_third
   
    return tickerData
