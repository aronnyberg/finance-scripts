#CURRENT ITERATIONS WILL LOOK BACK 10(lookback) * 1(steps), sort the best 20 convexity pairs, and deliver a 1 if convexity is still delivered in the next 1 * 1 periods
# and a -1 if the convex profile flips to concavity.

import pandas as pd
import numpy as np
df = pd.read_pickle('ALL YOUR DATA.pkl') #ALTER PICKLE FILE FOR CSV ETC
def logRets(vals):
    vals = vals.dropna()
    ret = vals/vals.shift(1) -1
    logRet = np.log(1+ret)
    return logRet
def get_payoff(x, y):
    #r = np.polyfit(x, y, 1)
    r2 = np.polyfit(x, y, 2)
    return r2
    
df2 = df.fillna(method='ffill').dropna(axis=1)
rets = logRets(df2).dropna(axis=0)
rets2 = rets
index = rets2.mean(axis=1)

def conv_metric(steps):
    conv_list = []
    stock_list = []
    date_list = []
    days = steps
    for i in range(days, len(rets2), days):
        for stock in rets2.columns:
            date_list.append(rets2.iloc[:,1].index[i])
            conv_list.append(get_payoff(index[i-days:i], rets2[stock][i-days:i])[0])
            stock_list.append(stock)
    return pd.DataFrame({'Date':date_list, 'Stock':stock_list, 'Convexity':conv_list}).set_index('Date')
    
conv20day = conv_metric(1)
convdf = conv20day.pivot_table(index='Date', columns='Stock', values='Convexity')


#Convexity Trading
pair_list = []
pair_returns_list = []
pair_conv_returns_list = []
date_list = []
trades = 10
backlook = 10
forwardlook = 5
for i in range(0, len(convdf)-forwardlook-1):
    
    date = convdf.index.values[i]
    #sorts = convdf.iloc[i,:].sort_values(ascending=True).index.values
    conv_sorts = convdf.iloc[i-backlook:i,:].mean(axis=0).sort_values(ascending=True).index.values
    #conv_sorts = convdf.iloc[0:i,:].mean(axis=0).sort_values(ascending=True).index.values #Can here switch to using all previous data to make decision
    top = conv_sorts[:trades]
    bottom = conv_sorts[-trades:]
    top_returns = rets2[top].iloc[i+1:i+forwardlook+1,:]
    bottom_returns = rets2[bottom].iloc[i+1:i+forwardlook+1,:]
    top_conv_returns = convdf[top].iloc[i+1:i+forwardlook+1,:]
    bottom_conv_returns = convdf[bottom].iloc[i+1:i+forwardlook+1,:]
    for stockpair in range(0,trades):
        pair_returns = np.mean(top_returns.values.T[stockpair]-bottom_returns.values.T[stockpair])
        pair_conv_returns = np.sign(np.sum(top_conv_returns.values.T[stockpair]-bottom_conv_returns.values.T[stockpair]))
        pair_returns_list.append(pair_returns)
        pair_conv_returns_list.append(pair_conv_returns)
        pair_list.append((top[stockpair], bottom[stockpair]))
        date_list.append(date)
        #pair_list.append()
        
df3 = pd.DataFrame({'Date':date_list, 'Pair Returns':pair_returns_list, 'Pair Convexity Returns':pair_conv_returns_list,
             'Date':date_list, 'Symbols':pair_list}).set_index(['Date', 'Symbols'])
df3['Pair Convexity Returns'].unstack().sum(axis=1).cumsum().plot()
             
