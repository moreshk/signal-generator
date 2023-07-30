import utils

def identify_trenddown(tickerData):
    """Identify Evening Star pattern."""
    downtrend = utils.identify_downtrend(tickerData,1,9,3)

    tickerData['DOWN'] = downtrend['Downtrend']
    return tickerData
