from matplotlib.pyplot import get
import pandas as pd
import numpy as np
from yahoo_fin import stock_info

#last 5 rows useless
def get_daily_data(tickerList):

    #This is the data-grabbing code, will take a long time 
    list_of_data = []
    for i in tickerList:
        try: 
            data = stock_info.get_data(i)
            list_of_data.append(data)
        except:
            pass

    #Following is organising the data and putting it in a dataframe
    df = pd.concat(list_of_data)
    return df

#get_daily_data('VOO')