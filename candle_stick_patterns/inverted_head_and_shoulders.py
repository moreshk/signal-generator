import utils
import numpy as np

def identify_inverted_head_and_shoulders(data, window=5):
    # Add the original date index to the DataFrame
    data['Date'] = data.index
    
    # Initialize the list to hold the indices of the peaks and troughs
    peaks = []
    troughs = []
    
    # Loop over the data
    for i in range(window, len(data) - window):
        # Get the prices for the current window
        prices = data['Close'].iloc[i - window:i + window]
        
        # Check if the current price is a peak
        if all(i < prices.iloc[window] for i in prices.iloc[:window]) and all(i < prices.iloc[window] for i in prices.iloc[window + 1:]):
            peaks.append((i, prices.iloc[window]))
            
        # Check if the current price is a trough
        if all(i > prices.iloc[window] for i in prices.iloc[:window]) and all(i > prices.iloc[window] for i in prices.iloc[window + 1:]):
            troughs.append((i, prices.iloc[window]))
    
    # Initialize the DataFrame to hold the head and shoulders patterns
    patterns = []

    # Loop over the troughs to find the inverted head and shoulders patterns
    # for i in range(1, len(troughs) - 1):
    #     # Get the indices of the left shoulder, head, and right shoulder
    #     ls_index, ls_price = troughs[i - 1]
    #     h_index, h_price = troughs[i]
    #     rs_index, rs_price = troughs[i + 1]
        
    #     # Check if the prices form an inverted head and shoulders pattern
    #     if ls_price > h_price and rs_price > h_price and np.isclose(ls_price, rs_price, rtol=0.05):
    #         # Find the peaks before and after the head
    #         before_head = [t for t in peaks if ls_index < t[0] < h_index]
    #         after_head = [t for t in peaks if h_index < t[0] < rs_index]
            
    #         # Check if there are peaks before and after the head
    #         if before_head and after_head:
    #             # Get the indices and prices of the peaks
    #             bh_index, bh_price = before_head[0]
    #             ah_index, ah_price = after_head[0]
                
    #             # Check if the peaks form a neckline
    #             if np.isclose(bh_price, ah_price, rtol=0.05) and rs_price < ah_price:
    #                 data = utils.identify_downtrend(data, 1, 20, .3)  # Added the deviation of 3%
    #                 if data['Downtrend'][ls_index - 1]:  # Check the candle immediately before the left shoulder
    #                     # Add the pattern to the patterns list
    #                     pattern = {'Left Shoulder': (ls_index, ls_price), 'Head': (h_index, h_price), 'Right Shoulder': (rs_index, rs_price), 'Neckline': [(bh_index, bh_price), (ah_index, ah_price)]}
    #                     patterns.append(pattern)

# Loop over the troughs to find the inverted head and shoulders patterns
    for i in range(1, len(troughs) - 1):
        # Get the indices of the left shoulder and head
        ls_index, ls_price = troughs[i - 1]
        h_index, h_price = troughs[i]
        
        # Find the peaks before and after the head
        before_head = [t for t in peaks if ls_index < t[0] < h_index]
        after_head = [t for t in peaks if h_index < t[0]]
        
        # Check if there are peaks before and after the head
        if before_head and after_head:
            # Get the indices and prices of the peaks
            bh_index, bh_price = before_head[0]
            ah_index, ah_price = after_head[0]
            
            # Find the right shoulder as the lowest point after the second peak but before the next peak
            after_second_peak = [t for t in troughs if ah_index < t[0] < after_head[1][0]] if len(after_head) > 1 else [t for t in troughs if ah_index < t[0]]
            if not after_second_peak:
                continue
            rs_index, rs_price = min(after_second_peak, key=lambda x: x[1])
            
            # Check if the prices form an inverted head and shoulders pattern
            if ls_price > h_price and rs_price > h_price and np.isclose(ls_price, rs_price, rtol=0.05) and rs_price < ah_price:
                data = utils.identify_downtrend(data, 1, 20, .3)  # Added the deviation of 3%
                if data['Downtrend'][ls_index - 1]:  # Check the candle immediately before the left shoulder
                    # Add the pattern to the patterns list
                    pattern = {'Left Shoulder': (ls_index, ls_price), 'Head': (h_index, h_price), 'Right Shoulder': (rs_index, rs_price), 'Neckline': [(bh_index, bh_price), (ah_index, ah_price)]}
                    patterns.append(pattern)

    return patterns
