import talib
import yfinance as yf

# Download the historical data
df = yf.download('AAPL', '2020-01-01', '2021-01-01')

# Compute the patterns
df['Doji'] = talib.CDLDOJI(df['Open'], df['High'], df['Low'], df['Close'])
df['Hammer'] = talib.CDLHAMMER(df['Open'], df['High'], df['Low'], df['Close'])
df['Engulfing'] = talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])
df['Morning Star'] = talib.CDLMORNINGSTAR(df['Open'], df['High'], df['Low'], df['Close'])
df['Shooting Star'] = talib.CDLSHOOTINGSTAR(df['Open'], df['High'], df['Low'], df['Close'])

# Show the patterns
print(df[df['Doji'] != 0])
print(df[df['Hammer'] != 0])
print(df[df['Engulfing'] != 0])
print(df[df['Morning Star'] != 0])
print(df[df['Shooting Star'] != 0])
