import pandas as pd

def identify_bullish_engulfing(tickerData):
    """Identify Bullish Engulfing patterns."""
    # Criteria for Bullish Engulfing pattern
    bullish_engulfing = (tickerData['Close'].shift(1) < tickerData['Open'].shift(1)) & \
                        (tickerData['Close'] > tickerData['Open']) & \
                        (tickerData['Open'] < tickerData['Close'].shift(1)) & \
                        (tickerData['Close'] > tickerData['Open'].shift(1))

    # Add new column for Bullish Engulfing pattern
    tickerData['Bullish Engulfing'] = bullish_engulfing

    return tickerData
