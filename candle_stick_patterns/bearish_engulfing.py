import pandas as pd

def identify_bearish_engulfing(tickerData):
    """Identify Bearish Engulfing patterns."""
    # Criteria for Bearish Engulfing pattern
    bearish_engulfing = (tickerData['Close'].shift(1) > tickerData['Open'].shift(1)) & \
                        (tickerData['Close'] < tickerData['Open']) & \
                        (tickerData['Open'] > tickerData['Close'].shift(1)) & \
                        (tickerData['Close'] < tickerData['Open'].shift(1))

    # Add new column for Bearish Engulfing pattern
    tickerData['Bearish Engulfing'] = bearish_engulfing

    return tickerData
