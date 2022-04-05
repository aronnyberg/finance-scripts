import pandas as pd
import numpy as np

def cleanDFdailyYahooStockPrices(df):
    df = df.replace(0,np.nan)
    
    # All price data to floats
    df[['open', 'high', 'close', 'adjclose', 'volume']] = df[['open', 
    'high', 'close', 'adjclose', 'volume']].astype(float, errors = 'raise')
    
    for index, row in df.iterrows():
        if row.loc['high'] < row.loc['close']:
            if row.loc['high'] < row.loc['low']:
                # close and low too high, so high probably wrong
                row.loc['high'] = np.nan
            #then high lower than low, but high higher than low, so close probably wrong
            else:
                row.loc['close'] = np.nan

        if row.loc['low'] < row.loc['close']:
            if row.loc['low'] < row.loc['high']:
                # close and low too high, so high probably wrong
                row.loc['low'] = np.nan
            #then high lower than low, but high higher than low, so close probably wrong
            else:
                row.loc['close'] = np.nan
    return df
        

    # Clean by looking at variances of o,h,l,c 
    # Highs should be at least as high as closes and etc
