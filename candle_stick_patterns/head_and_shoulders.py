# import numpy as np

# def identify_head_and_shoulders(data, window=5):
#     # Add the original date index to the DataFrame
#     data['Date'] = data.index
#     # Initialize the list to hold the indices of the peaks and troughs
#     peaks = []
#     troughs = []
    
#     # Loop over the data
#     for i in range(window, len(data) - window):
#         # Get the prices for the current window
#         prices = data['Close'].iloc[i - window:i + window]
        
#         # Check if the current price is a peak
#         if all(i < prices.iloc[window] for i in prices.iloc[:window]) and all(i < prices.iloc[window] for i in prices.iloc[window + 1:]):
#             peaks.append((i, prices.iloc[window]))
            
#         # Check if the current price is a trough
#         if all(i > prices.iloc[window] for i in prices.iloc[:window]) and all(i > prices.iloc[window] for i in prices.iloc[window + 1:]):
#             troughs.append((i, prices.iloc[window]))
    
#     # Initialize the DataFrame to hold the head and shoulders patterns
#     data['Left Shoulder'] = np.nan
#     data['Head'] = np.nan
#     data['Right Shoulder'] = np.nan
#     data['Neckline'] = np.nan
#     data['Intersection'] = np.nan
    
#     # Loop over the peaks to find the head and shoulders patterns
#     for i in range(1, len(peaks) - 1):
#         # Get the indices of the left shoulder, head, and right shoulder
#         ls_index, ls_price = peaks[i - 1]
#         h_index, h_price = peaks[i]
#         rs_index, rs_price = peaks[i + 1]
        
#         # Check if the prices form a head and shoulders pattern
#         if ls_price < h_price and rs_price < h_price and np.isclose(ls_price, rs_price, rtol=0.05):
#             # Find the troughs before and after the head
#             before_head = [t for t in troughs if ls_index < t[0] < h_index]
#             after_head = [t for t in troughs if h_index < t[0] < rs_index]
            
#             # Check if there are troughs before and after the head
#             if before_head and after_head:
#                 # Get the indices and prices of the troughs
#                 bh_index, bh_price = before_head[0]
#                 ah_index, ah_price = after_head[0]
                
#                 # Check if the troughs form a neckline
#                 if np.isclose(bh_price, ah_price, rtol=0.05):
#                     # Add the pattern to the DataFrame
#                     data.loc[ls_index, 'Left Shoulder'] = ls_price
#                     data.loc[h_index, 'Head'] = h_price
#                     data.loc[rs_index, 'Right Shoulder'] = rs_price
#                     data.loc[bh_index:ah_index, 'Neckline'] = np.linspace(bh_price, ah_price, ah_index - bh_index + 1)
                    
#                     # Find the intersection of the neckline and the prices after the right shoulder
#                     for i in range(rs_index + 1, len(data)):
#                         if data['Close'].iloc[i] < data['Neckline'].iloc[i]:
#                             data.loc[i, 'Intersection'] = data['Close'].iloc[i]
#                             break
    
#     return data
import numpy as np

def identify_head_and_shoulders(data, window=5):
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

    # Loop over the peaks to find the head and shoulders patterns
    for i in range(1, len(peaks) - 1):
        # Get the indices of the left shoulder, head, and right shoulder
        ls_index, ls_price = peaks[i - 1]
        h_index, h_price = peaks[i]
        rs_index, rs_price = peaks[i + 1]
        
        # Check if the prices form a head and shoulders pattern
        if ls_price < h_price and rs_price < h_price and np.isclose(ls_price, rs_price, rtol=0.05):
            # Find the troughs before and after the head
            before_head = [t for t in troughs if ls_index < t[0] < h_index]
            after_head = [t for t in troughs if h_index < t[0] < rs_index]
            
            # Check if there are troughs before and after the head
            if before_head and after_head:
                # Get the indices and prices of the troughs
                bh_index, bh_price = before_head[0]
                ah_index, ah_price = after_head[0]
                
                # Check if the troughs form a neckline
                if np.isclose(bh_price, ah_price, rtol=0.05):
                    # Add the pattern to the patterns list
                    pattern = {'Left Shoulder': (ls_index, ls_price), 'Head': (h_index, h_price), 'Right Shoulder': (rs_index, rs_price), 'Neckline': [(bh_index, bh_price), (ah_index, ah_price)]}
                    patterns.append(pattern)

    return patterns
