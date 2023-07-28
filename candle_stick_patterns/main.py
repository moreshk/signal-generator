from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from hammer import identify_hammer
from hanging_man import identify_hanging_man
from utils import calculate_body_and_shadow
from plot_chart import plot_chart
from marubozu import identify_marubozu
from bullish_engulfing import identify_bullish_engulfing
from bearish_engulfing import identify_bearish_engulfing
from inverted_hammer import identify_inverted_hammer
from piercing_line import identify_piercing_line
from bullish_hammer import identify_bullish_hammer
from bullish_harami import identify_bullish_harami
from bearish_harami import identify_bearish_harami

import os

# Define the ticker symbol
tickerSymbol = '^NSEI'

# Get today's date
endDate = datetime.now()

# Get the data for the desired period
startDate = endDate - timedelta(days=720)  # change to your desired period

# Define the file name for storing the data
fileName = f"{tickerSymbol}_data_{startDate.strftime('%Y%m%d')}_{endDate.strftime('%Y%m%d')}.csv"

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
tickerData = calculate_body_and_shadow(tickerData)

# Identify patterns
tickerData = identify_hammer(tickerData)
tickerData = identify_hanging_man(tickerData)
tickerData = identify_marubozu(tickerData)
tickerData = identify_bullish_engulfing(tickerData)
tickerData = identify_bearish_engulfing(tickerData)
tickerData = identify_inverted_hammer(tickerData)
tickerData = identify_piercing_line(tickerData)
tickerData = identify_bullish_hammer(tickerData)
tickerData = identify_bullish_harami(tickerData)
tickerData = identify_bearish_harami(tickerData)

# Plot the chart
plot_chart(tickerData)