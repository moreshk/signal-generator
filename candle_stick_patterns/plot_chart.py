import plotly.graph_objects as go
import numpy as np

def plot_chart(tickerData, patterns, selected_pattern=None):
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
    pattern_names = ['Hammer', 'Hanging Man', 'Bullish Full Marubozu', 'Bullish Open Marubozu', 'Bullish Close Marubozu', 
                'Bearish Full Marubozu', 'Bearish Open Marubozu', 'Bearish Close Marubozu', 'Bullish Engulfing', 
                'Bearish Engulfing', 'Inverted Hammer', 'Piercing Line', 'Bullish Harami', 'Bearish Harami', 
                'Shooting Star', 'Morning Star', 'Evening Star', 'UP', 'DOWN', 'Morning Doji Star', 'Evening Doji Star',
                'Dark Cloud Cover', 'Tweezer Bottom', 'Tweezer Top']  # Added 'Trend'

    symbols = ['star', 'x', 'circle', 'cross', 'diamond', 'square', 'triangle-up', 'triangle-down', 'pentagon', 
            'hexagon', 'y-up', 'y-down', 'octagon', 'star-diamond', 'hourglass', 'bowtie', 'hash', 'arrow-up', 
            'arrow-down', 'square-dot', 'diamond-dot', 'cross-open', 'hexagram', 'hexagram-open']  # Added 'plus' for 'Trend'

    for pattern, symbol in zip(pattern_names, symbols):
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

    # Add head and shoulders pattern markers
    for i, pattern in enumerate(patterns):
        # Add the left shoulder, head, and right shoulder
        # for point in ['Left Shoulder', 'Head', 'Right Shoulder']:
        #     index, price = pattern[point]
        #     fig.add_trace(go.Scatter(x=[tickerData.index[index]], y=[price], mode='markers', name=f'{point} {i + 1}', visible='legendonly'))

        # Add the neckline
        start, end = pattern['Neckline']
        slope = (end[1] - start[1]) / (end[0] - start[0])

        # Extend the neckline to the right until it intersects a candlestick
        extended_end = end
        for j in range(end[0] + 1, len(tickerData)):
            extended_price = end[1] + slope * (j - end[0])
            if extended_price <= tickerData['High'][j] and extended_price >= tickerData['Low'][j]:
                extended_end = (j, extended_price)
                break

        # Add the extended neckline
        x = [tickerData.index[start[0]], tickerData.index[extended_end[0]]]
        y = [start[1], extended_end[1]]
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'Neckline {i + 1}', visible='legendonly', line=dict(width=4)))

        # Add lines connecting the points of the pattern
        x = [tickerData.index[pattern['Left Shoulder'][0]], tickerData.index[start[0]], 
             tickerData.index[pattern['Head'][0]], tickerData.index[end[0]], 
             tickerData.index[pattern['Right Shoulder'][0]], tickerData.index[extended_end[0]]]
        y = [pattern['Left Shoulder'][1], start[1], pattern['Head'][1], end[1], pattern['Right Shoulder'][1], extended_end[1]]
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'Pattern {i + 1}', visible='legendonly', line=dict(width=4)))

    fig.update_layout(
        yaxis_title='Price',
        xaxis_title='Date',
        xaxis=dict(
            rangeslider=dict(visible=True),
            type='category'   # this line will remove the gaps for non-trading days
        ),
    )

    # Show the figure
    fig.show()
