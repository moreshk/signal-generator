import utils

# def identify_uptrend(tickerData):
#     """Identify an uptrend, where at least 3 out of the 5 prior candles are bullish."""
#     bullish = [tickerData['Close'].shift(i) > tickerData['Open'].shift(i) for i in range(3, 8)]
#     tickerData['Uptrend'] = sum(bullish) >= 3
#     return tickerData

def identify_evening_star(tickerData):
    """Identify Evening Star pattern."""
    tickerData = utils.calculate_body_and_doji(tickerData)
    # tickerData = identify_uptrend(tickerData)
    uptrend = utils.identify_uptrend(tickerData,3,3,.1)
    
    first_candle_bullish = tickerData['Close'].shift(2) > tickerData['Open'].shift(2)
    first_candle_not_doji = ~(tickerData['Doji'].shift(2).fillna(False).astype(bool))   # First candle is not a doji
    second_candle_doji = tickerData['Doji'].shift(1)
    gap_up_first_second = tickerData['Open'].shift(1) > tickerData['Close'].shift(2)
    third_candle_bearish = tickerData['Open'] > tickerData['Close']
    third_candle_not_doji = ~(tickerData['Doji'].fillna(False).astype(bool))   # Third candle is not a doji
    gap_down_second_third = tickerData['Open'] < tickerData['Close'].shift(1)

    tickerData['Evening Star'] = uptrend['Uptrend'] & first_candle_bullish & first_candle_not_doji & second_candle_doji & gap_up_first_second & third_candle_bearish & third_candle_not_doji & gap_down_second_third
    # tickerData['Evening Star'] = first_candle_bullish & first_candle_not_doji & second_candle_doji & gap_up_first_second & third_candle_bearish & third_candle_not_doji & gap_down_second_third
    
    return tickerData
