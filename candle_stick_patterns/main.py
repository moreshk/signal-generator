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
from shooting_star import identify_shooting_star
from morning_star import identify_morning_star
from evening_star import identify_evening_star
from uptrend_detector import identify_trendup
from downtrend_detector import identify_trenddown
from morning_doji_star import identify_morning_doji_star
from evening_doji_star import identify_evening_doji_star
from dark_cloud_cover import identify_dark_cloud_cover
from tweezer_bottom import identify_tweezer_bottom
from tweezer_top import identify_tweezer_top
from head_and_shoulders import identify_head_and_shoulders
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
tickerData = identify_shooting_star(tickerData)
tickerData = identify_morning_star(tickerData)
tickerData = identify_evening_star(tickerData)
tickerData = identify_trendup(tickerData)
tickerData = identify_trenddown(tickerData)
tickerData = identify_morning_doji_star(tickerData)
tickerData = identify_evening_doji_star(tickerData)
tickerData = identify_dark_cloud_cover(tickerData)
tickerData = identify_tweezer_bottom(tickerData)
tickerData = identify_tweezer_top(tickerData)

# Convert the index to integers for pattern detection
tickerData.reset_index(drop=True, inplace=True)

patterns = identify_head_and_shoulders(tickerData)

# Convert the index back to dates
tickerData.set_index('Date', inplace=True)

# Plot the chart
plot_chart(tickerData, patterns)