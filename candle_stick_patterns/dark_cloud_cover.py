import pandas as pd
import numpy as np
import utils

def identify_dark_cloud_cover(tickerData):
    """Identify Dark Cloud Cover patterns."""
    
    # Check for an upward trend in the past 5 days
    uptrend = utils.identify_uptrend(tickerData,2,5,.3)

    # Check for a bullish candle followed by a bearish candle
    bullish_bearish = (tickerData['Open'].shift(1) < tickerData['Close'].shift(1)) & \
                      (tickerData['Open'] > tickerData['Close'])

    # Check if the second candle opened higher than the first candle's high
    second_candle_open_higher = tickerData['Open'] > tickerData['High'].shift(1)

    # Calculate the midpoint of the body of the first candle
    first_candle_body_mid = (tickerData['Open'].shift(1) + tickerData['Close'].shift(1)) / 2

    # Check if the second candle closed below the midpoint of the body of the first candle
    second_candle_close_lower = tickerData['Close'] < first_candle_body_mid

    # Check if the second candle closed above the open of the first candle
    second_candle_close_above_open = tickerData['Close'] > tickerData['Open'].shift(1)

    # Check for big bodies
    big_bodies = np.abs((tickerData['Close'] - tickerData['Open']) / tickerData['Open']) > 0.01

    # Combine all the conditions to identify the Dark Cloud Cover pattern
    dark_cloud_cover = uptrend['Uptrend'] & bullish_bearish & second_candle_open_higher & \
                       second_candle_close_lower & second_candle_close_above_open & big_bodies

    # Add new column for Dark Cloud Cover pattern
    tickerData['Dark Cloud Cover'] = dark_cloud_cover

    return tickerData
