import pandas as pd
from yahoo_fin import stock_info#yahoo finance data API
from matplotlib import pyplot as plt
import numpy as np
def logRets(vals):
    vals = vals.dropna()
    ret = vals/vals.shift(1) -1
    logRet = np.log(1+ret)
    return logRet
def get_payoff(x, y):
    a = x
    b = y
    r = np.polyfit(a, b, 1)
    r2 = np.polyfit(a, b, 2)
    plt.plot(a, b, 'o')
    plt.plot(a,np.polyval(r, a), 'r-')
    plt.plot(a,np.polyval(r2, a), 'b--')
    plt.ylabel(y.name)
    plt.xlabel(x.name)
    
iwn = stock_info.get_data('IWN')
spy = stock_info.get_data('SPY')

iwn = iwn.rename(columns={'close':'IWN'})
spy = spy.rename(columns={'close':'SPY'})
df = pd.concat([logRets(iwn['IWN']), logRets(spy['SPY'])], axis=1)

df = df.dropna(axis=0)
get_payoff(df['SPY'], df['IWN'])
