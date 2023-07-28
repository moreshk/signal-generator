import plotly.graph_objects as go

def plot_chart(tickerData, selected_pattern=None):
    """Create a candlestick chart with pattern markers and colored candles."""
    fig = go.Figure()

    fig.add_trace(go.Candlestick(x=tickerData.index,
                                 open=tickerData['Open'],
                                 high=tickerData['High'],
                                 low=tickerData['Low'],
                                 close=tickerData['Close'],
                                 increasing_line_color='blue',   
                                 decreasing_line_color='black',
                                 name='Price'))

    # Add pattern markers
    patterns = ['Hammer', 'Hanging Man', 'Bullish Full Marubozu', 'Bullish Open Marubozu', 'Bullish Close Marubozu', 
            'Bearish Full Marubozu', 'Bearish Open Marubozu', 'Bearish Close Marubozu', 'Bullish Engulfing', 
            'Bearish Engulfing', 'Inverted Hammer', 'Piercing Line', 'Bullish Harami', 'Bearish Harami', 
            'Shooting Star', 'Morning Star', 'Evening Star']  # Added 'Morning Star' and 'Evening Star'

    symbols = ['star', 'x', 'circle', 'cross', 'diamond', 'square', 'triangle-up', 'triangle-down', 'pentagon', 
        'hexagon', 'y-up', 'y-down', 'octagon', 'star-diamond', 'hourglass', 'bowtie', 'hash']  # Added 'bowtie' for 'Morning Star' and 'hash' for 'Evening Star'

    for pattern, symbol in zip(patterns, symbols):
        if "Bearish" in pattern:
            y_location = 'Low'
        else:
            y_location = 'High'
        pattern_trace = go.Scatter(x=tickerData[tickerData[pattern]].index,
                                   y=tickerData[tickerData[pattern]][y_location],
                                   mode='markers',
                                   marker_symbol=symbol,
                                   marker_size=10,  # Adjust the size as needed
                                   marker_line_width=2,
                                   marker_line_color='red',  # Line color is now red for visibility
                                   name=pattern,
                                   visible='legendonly')
        fig.add_trace(pattern_trace)

    fig.update_layout(
        title='NIFTY index - last 120 days',
        yaxis_title='Price',
        xaxis_title='Date',
        xaxis=dict(
            rangeslider=dict(visible=False),
            type='category'   # this line will remove the gaps for non-trading days
        ),
    )


    # Show the figure
    fig.show()
