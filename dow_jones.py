import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# Define the ticker symbol
tickerSymbol = '^DJI'

# Get today's date
endDate = datetime.now()

# Get the data for the past 30 days
startDate = endDate - timedelta(days=60)
tickerData = yf.download(tickerSymbol, start=startDate, end=endDate)
tickerData = tickerData.round(2)

tickerData = tickerData.drop(['High', 'Low', 'Volume'], axis=1)

print(tickerData)

# Update endDate to be the latest date in tickerData
endDate = tickerData.index.max()

# Calculate start and end values
def get_values(df):
    start_open = df.iloc[0]['Open']
    start_close = df.iloc[0]['Close']
    start_adj_close = df.iloc[0]['Adj Close']

    end_open = df.iloc[-1]['Open']
    end_close = df.iloc[-1]['Close']
    end_adj_close = df.iloc[-1]['Adj Close']

    return start_open, start_close, start_adj_close, end_open, end_close, end_adj_close

# Define a function that takes in the start close and end open values
# and returns 'UP' if the end open is greater than the start close,
# 'DOWN' if it's less, and 'FLAT' if they are equal
def calculate_trend(start_close, end_open):
    if end_open > start_close:
        return 'UP'
    elif end_open < start_close:
        return 'DOWN'
    else:
        return 'FLAT'
    
# Daily Data
dailyData = tickerData.iloc[-2:]

# Weekly Data
weeklyData = tickerData.iloc[-5:-1]

# Monthly Data
monthlyData = tickerData.iloc[-22:-1]

# Get values for each period
dailyValues = get_values(dailyData)
weeklyValues = get_values(weeklyData)
monthlyValues = get_values(monthlyData)

# Calculate start dates
dailyStartDate = tickerData.index[-2]
weeklyStartDate = tickerData.index[-5]  # Fix: use the actual start date of the week from resampled data
monthlyStartDate = tickerData.index[-22]  # Fix: use the actual start date of the month from resampled data

# Ensure these are dates and not datetimes
dailyStartDate = dailyStartDate.date()
weeklyStartDate = weeklyStartDate.date()
monthlyStartDate = monthlyStartDate.date()
endDate = endDate.date()

# Create a new dataframe for display
data = {
    'Start Date': [dailyStartDate, weeklyStartDate, monthlyStartDate],
    'End Date': [endDate, endDate, endDate],
    'Start Date Open': [dailyValues[0], weeklyValues[0], monthlyValues[0]],
    'Start Date Close': [dailyValues[1], weeklyValues[1], monthlyValues[1]],
    'Start Date Adjusted Close': [dailyValues[2], weeklyValues[2], monthlyValues[2]],
    'End Date Open': [dailyValues[3], dailyValues[3], dailyValues[3]],  # Fix: Always use dailyValues for end date
    'End Date Close': [dailyValues[4], dailyValues[4], dailyValues[4]],  # Fix: Always use dailyValues for end date
    'End Date Adjusted Close': [dailyValues[5], dailyValues[5], dailyValues[5]]  # Fix: Always use dailyValues for end date
}

df = pd.DataFrame(data, index=['Daily', 'Weekly', 'Monthly'])

# Apply the function to the 'Start Date Close' and 'End Date Open' columns
df['Trend'] = df.apply(lambda row: calculate_trend(row['Start Date Adjusted Close'], row['End Date Adjusted Close']), axis=1)

df = df.round(2)

print(df)
