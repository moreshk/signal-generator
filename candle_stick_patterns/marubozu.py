def identify_marubozu(tickerData, epsilon=0.0002):
    """Identify Marubozu patterns."""
    # Criteria for bullish Marubozu patterns
    bullish_full = (tickerData['Open'] <= tickerData['Low'] * (1 + epsilon)) & (tickerData['Close'] >= tickerData['High'] * (1 - epsilon))
    bullish_open = (tickerData['Open'] <= tickerData['Low'] * (1 + epsilon)) & (tickerData['Close'] < tickerData['High'])
    bullish_close = (tickerData['Open'] > tickerData['Low']) & (tickerData['Close'] >= tickerData['High'] * (1 - epsilon))

    # Criteria for bearish Marubozu patterns
    bearish_full = (tickerData['Open'] >= tickerData['High'] * (1 - epsilon)) & (tickerData['Close'] <= tickerData['Low'] * (1 + epsilon))
    bearish_open = (tickerData['Open'] >= tickerData['High'] * (1 - epsilon)) & (tickerData['Close'] > tickerData['Low'])
    bearish_close = (tickerData['Open'] < tickerData['High']) & (tickerData['Close'] <= tickerData['Low'] * (1 + epsilon))

    # Add new columns for Marubozu patterns
    tickerData['Bullish Full Marubozu'] = bullish_full
    tickerData['Bullish Open Marubozu'] = bullish_open
    tickerData['Bullish Close Marubozu'] = bullish_close

    tickerData['Bearish Full Marubozu'] = bearish_full
    tickerData['Bearish Open Marubozu'] = bearish_open
    tickerData['Bearish Close Marubozu'] = bearish_close

    return tickerData
