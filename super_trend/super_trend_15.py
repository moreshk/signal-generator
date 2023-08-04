import yfinance as yf
import dash
from dash.dependencies import Output, Input
from dash import dcc, html
import plotly.graph_objects as go
import pandas_ta as ta

# Create a dash application
app = dash.Dash(__name__)

# Define the layout
# Add a style argument to set the height
app.layout = html.Div(
    [
        dcc.Interval(id='interval-component', interval=15*60000, n_intervals=0),  # 1 minute intervals
        dcc.Graph(id='live-graph', style={'height': 'calc(100vh - 20px)'})
    ]
)

# Callback to update the graph
@app.callback(Output('live-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph(n):

    # Download 15 minute data for past 5 days 
    nse = yf.Ticker("^NSEI")
    hist = nse.history(period="5d", interval="15m")

    # Calculate Supertrend
    supertrend = hist.ta.supertrend(length=7, multiplier=3)
    hist['SUPERTl_7_3.0'] = supertrend['SUPERTl_7_3.0']
    hist['SUPERTs_7_3.0'] = supertrend['SUPERTs_7_3.0']

    # Print column names
    print(hist.columns)
    
    # Remove gaps between trading days
    hist = hist.between_time('09:15', '15:30')

    # Format datetime index
    hist.index = hist.index.strftime('%d-%m-%Y %H:%M')

    # Create candlestick chart 
    fig = go.Figure(data=[go.Candlestick(x=hist.index, 
                    open=hist['Open'], 
                    high=hist['High'],
                    low=hist['Low'], 
                    close=hist['Close'])])

    
    # Add Supertrend lines
    fig.add_trace(go.Scatter(x=hist.index, y=hist['SUPERTl_7_3.0'], mode='lines', name='Supertrend Lower'))
    fig.add_trace(go.Scatter(x=hist.index, y=hist['SUPERTs_7_3.0'], mode='lines', name='Supertrend Upper'))
    
    fig.update_layout(
        yaxis_title='Index Value',
        xaxis_rangeslider_visible=False,
        xaxis_type='category'  # Treat x-axis as category to remove gaps
    )

    return fig

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True)
