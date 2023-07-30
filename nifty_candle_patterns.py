import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go

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

def identify_hanging_man(tickerData):
    """Identify Hanging Man pattern."""
    tickerData['Hanging Man'] = ((tickerData['Body'].shift(1) < tickerData['Body'].shift(2)) &
                                  (tickerData['Close'] > tickerData['Open']) &
                                  (tickerData['Lower Shadow'] >= 2 * tickerData['Body']))
    return tickerData

def plot_chart(tickerData):
    """Create a candlestick chart with Bullish Hammer and Hanging Man markers."""
    fig = go.Figure(data=[go.Candlestick(x=tickerData.index,
                                         open=tickerData['Open'],
                                         high=tickerData['High'],
                                         low=tickerData['Low'],
                                         close=tickerData['Close'],
                                         increasing_line_color= 'blue', 
                                         decreasing_line_color= 'black',
                                         name='Price')])

    # Add Bullish Hammer pattern markers
    hammer = go.Scatter(x=tickerData[tickerData['Bullish Hammer']].index,
                        y=tickerData[tickerData['Bullish Hammer']]['High'],
                        mode='markers',
                        marker_symbol='star',
                        marker_size=8,
                        marker_color='yellow',
                        name='Bullish Hammer')

    # Add Hanging Man pattern markers
    hanging_man = go.Scatter(x=tickerData[tickerData['Hanging Man']].index,
                             y=tickerData[tickerData['Hanging Man']]['High'],
                             mode='markers',
                             marker_symbol='x',
                             marker_size=8,
                             marker_color='red',
                             name='Hanging Man')

    fig.add_trace(hammer)
    fig.add_trace(hanging_man)

    fig.update_layout(
        title='NIFTY index - last 120 days',
        yaxis_title='Price',
        xaxis_title='Date',
        xaxis_rangeslider_visible=False,
        xaxis=dict(
            type='category'   # this line will remove the gaps for non-trading days
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                active=0,
                x=0.57,
                y=1.2,
                buttons=list([
                    dict(label="Both",
                         method="update",
                         args=[{"visible": [True, True, True]},
                               {"title": "Bullish Hammer and Hanging Man"}]),
                    dict(label="Bullish Hammer",
                         method="update",
                         args=[{"visible": [True, True, False]},
                               {"title": "Bullish Hammer"}]),
                    dict(label="Hanging Man",
                         method="update",
                         args=[{"visible": [True, False, True]},
                               {"title": "Hanging Man"}]),
                ]),
            )
        ]
    )

    # Show the figure
    fig.show()

# Define the ticker symbol
tickerSymbol = '^NSEI'

# Get today's date
endDate = datetime.now()

# Get the data for the past 120 days
startDate = endDate - timedelta(days=120)
tickerData = yf.download(tickerSymbol, start=startDate, end=endDate)
tickerData = tickerData.round(2)

# Ensure the index is in datetime format
tickerData.index = pd.to_datetime(tickerData.index)

# Convert the dates into string format without time
tickerData.index = tickerData.index.strftime('%Y-%m-%d')

# Calculate body and shadow
tickerData = calculate_body_and_shadow(tickerData)

# Identify patterns
tickerData = identify_bullish_hammer(tickerData)
tickerData = identify_hanging_man(tickerData)

# Plot the chart
plot_chart(tickerData)

import plotly.graph_objects as go
import candle_stick_patterns.bullish_hammer as bh
import candle_stick_patterns.hanging_man as hm
import data_processing as dp

def plot_chart(tickerData):
    """Create a candlestick chart with Bullish Hammer and Hanging Man markers."""
    # Your previous plot_chart function here

# Define the ticker symbol
tickerSymbol = '^NSEI'

# Fetch and process data
tickerData = dp.fetch_data(tickerSymbol)

# Calculate body and shadow for each pattern
tickerData = bh.calculate_body_and_shadow(tickerData)
tickerData = hm.calculate_body_and_shadow(tickerData)

# Identify patterns
tickerData = bh.identify_bullish_hammer(tickerData)
tickerData = hm.identify_hanging_man(tickerData)

# Plot the chart
plot_chart(tickerData)
