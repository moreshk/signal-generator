import utils

def identify_trendup(tickerData):
    """Identify Evening Star pattern."""
    uptrend = utils.identify_uptrend(tickerData,1,9,3)

    tickerData['UP'] = uptrend['Uptrend']
    return tickerData
