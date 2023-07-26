from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from bullish_hammer import calculate_body_and_shadow as calc_bh, identify_bullish_hammer
from hanging_man import calculate_body_and_shadow as calc_hm, identify_hanging_man
from plot_chart import plot_chart
from marubozu import identify_marubozu
from bullish_engulfing import identify_bullish_engulfing
import os

# Define the ticker symbol
tickerSymbol = '^NSEI'

# Define the file name for storing the data
fileName = f"{tickerSymbol}_data.csv"

# Get today's date
endDate = datetime.now()

# Get the data for the past 360 days
startDate = endDate - timedelta(days=360)

# Check if data is already downloaded
if os.path.exists(fileName):
    # Load data from CSV file
    tickerData = pd.read_csv(fileName, parse_dates=True, index_col='Date')
else:
    # Download data if not already downloaded
    tickerData = yf.download(tickerSymbol, start=startDate, end=endDate)
    tickerData = tickerData.round(2)

    # Save data to CSV file
    tickerData.to_csv(fileName)

# Ensure the index is in datetime format
tickerData.index = pd.to_datetime(tickerData.index)

# Convert the dates into string format without time
tickerData.index = tickerData.index.strftime('%Y-%m-%d')

# Calculate body and shadow
tickerData = calc_bh(tickerData)
tickerData = calc_hm(tickerData)

# Identify patterns
tickerData = identify_bullish_hammer(tickerData)
tickerData = identify_hanging_man(tickerData)
tickerData = identify_marubozu(tickerData)
tickerData = identify_bullish_engulfing(tickerData)

# Plot the chart
plot_chart(tickerData)
