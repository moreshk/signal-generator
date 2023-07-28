import utils

def identify_downturn(tickerData):
    """Identify a downturn, where at least 4 out of the 6 prior candles are bearish."""
    bearish = [tickerData['Open'].shift(i) > tickerData['Close'].shift(i) for i in range(3, 9)]
    tickerData['Downturn'] = sum(bearish) >= 4
    return tickerData

def identify_morning_star(tickerData):
    """Identify Morning Star pattern."""
    tickerData = utils.calculate_body_and_doji(tickerData)
    tickerData = identify_downturn(tickerData)
    
    first_candle_bearish = tickerData['Open'].shift(2) > tickerData['Close'].shift(2)
    first_candle_not_doji = ~(tickerData['Doji'].shift(2).fillna(False).astype(bool))   # First candle is not a doji
    second_candle_doji = tickerData['Doji'].shift(1)
    gap_down_first_second = tickerData['Close'].shift(2) > tickerData['Open'].shift(1)
    third_candle_bullish = tickerData['Close'] > tickerData['Open']
    third_candle_not_doji = ~(tickerData['Doji'].fillna(False).astype(bool))   # Third candle is not a doji
    gap_up_second_third = tickerData['Close'].shift(1) < tickerData['Open']

    tickerData['Morning Star'] = tickerData['Downturn'] & first_candle_bearish & first_candle_not_doji & second_candle_doji & gap_down_first_second & third_candle_bullish & third_candle_not_doji & gap_up_second_third
    return tickerData