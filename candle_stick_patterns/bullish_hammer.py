def calculate_body_and_shadow(tickerData):
    """Calculate the body size and the lower shadow size."""
    tickerData['Body'] = abs(tickerData['Open'] - tickerData['Close'])
    tickerData['Lower Shadow'] = tickerData[['Open', 'Close']].min(axis=1) - tickerData['Low']
    return tickerData

def identify_bullish_hammer(tickerData):
    """Identify Bullish Hammer pattern."""
    tickerData['Bullish Hammer'] = ((tickerData['Body'].shift(1) > tickerData['Body'].shift(2)) &
                                     (tickerData['Close'] > tickerData['Open']) &
                                     (tickerData['Lower Shadow'] >= 2 * tickerData['Body']))
    return tickerData
