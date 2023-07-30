import pandas as pd
import numpy as np
import utils

def identify_piercing_line(tickerData):
    """Identify Piercing Line patterns."""
    
    # Check for a downward trend in the past 3 days
    # downtrend = (tickerData['Close'].shift(2) < tickerData['Close'].shift(3)) 
    # & \                 (tickerData['Close'].shift(3) < tickerData['Close'].shift(4))

    downtrend = utils.identify_downtrend(tickerData,2,5,.3)

    # Check for a bearish candle followed by a bullish candle
    bearish_bullish = (tickerData['Close'].shift(1) < tickerData['Open'].shift(1)) & \
                      (tickerData['Close'] > tickerData['Open'])

    # Check if the second candle opened lower than the first candle's low
    second_candle_open_lower = tickerData['Open'] < tickerData['Low'].shift(1)

    # # Check if the second candle closed above the close of the first candle
    # second_candle_close_higher = tickerData['Close'] > tickerData['Close'].shift(1)

     # Calculate the midpoint of the body of the first candle
    first_candle_body_mid = (tickerData['Close'].shift(1) + tickerData['Open'].shift(1)) / 2

    # Check if the second candle closed above the midpoint of the body of the first candle
    second_candle_close_higher = tickerData['Close'] > first_candle_body_mid

    # Check if the second candle closed below the open of the first candle
    second_candle_close_below_open = tickerData['Close'] < tickerData['Open'].shift(1)
    
    # Check for big bodies
    big_bodies = np.abs((tickerData['Close'] - tickerData['Open']) / tickerData['Open']) > 0.01

    # Combine all the conditions to identify the piercing line pattern
    piercing_line = downtrend['Downtrend'] & bearish_bullish & second_candle_open_lower & \
                    second_candle_close_higher & second_candle_close_below_open & big_bodies

    # Add new column for Piercing Line pattern
    tickerData['Piercing Line'] = piercing_line

    return tickerData
