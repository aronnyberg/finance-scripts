# Rebalancing calculator, meaning the expected return from rebalanced (fixed weight) and non-rebalanced (drift weight) strategies, to 
# which, the weighting and frequency of the rebalance can be altered. 
# Example below uses BTC/USD from FTX's free API
import pandas as pd
import numpy as np
import requests

#resolution = 3600 == 1 hour
#43200 = 12 hours
#86400 = 1 day
historical = requests.get('https://ftx.com/api/markets/BTC/USD/candles?resolution=86400').json()

data = pd.DataFrame(historical['result'])
data.drop(['startTime'], axis = 1, inplace=True)
data['time'] = pd.to_datetime(data['time'], unit='ms')
data.set_index('time', inplace=True)

data['pct'] = data['close'].pct_change()
data['n'] = [i+1 for i in range(len(data))]
data['ofWeek'] = data.index.dayofweek+1

#Actual tool below
def rebalance(data, weighting, wealth,rebalanceFreq, pcFeesPerRebalance, returnColumn):
    
    nominalTradeSize = weighting*wealth
    dailyReturn = 1+data[returnColumn]
    driftWeight = (np.cumprod(dailyReturn)*weighting)+(1-weighting)
    wealthList = []
    nominalTradeSizeList = [] #counts days as wel as stores nominal trade size
    weightingList = [] #checks if the rebalancing works
    for date in data.index[1:]:

        if len(nominalTradeSizeList) < rebalanceFreq:
            weightingList.append(nominalTradeSize/wealth) #checks if the rebalancing works
            nominalReturn = nominalTradeSize*(dailyReturn.loc[date]-1) # -1 so 1.01 becomes 0.01 ie a % change
            wealth += nominalReturn

            wealthList.append(wealth)
            nominalTradeSizeList.append(nominalTradeSize) #attach nominal trade size with it's assoicated return
            nominalTradeSize += nominalReturn #Computes tomorrows nominal trade size

        if len(nominalTradeSizeList) == rebalanceFreq:
            nominalTradeSizeList = []
            nominalTradeSize = wealth*weighting
            wealth -= pcFeesPerRebalance
            
    allDF = pd.DataFrame(driftWeight.dropna())
    allDF.columns = ['DriftWeight']
    allDF['FixedWeight'] = wealthList
    
    dwSharpe = allDF['DriftWeight'].mean()/allDF['DriftWeight'].std()
    fwSharpe = allDF['FixedWeight'].mean()/allDF['FixedWeight'].std()
    
    return (allDF['FixedWeight']-allDF['DriftWeight']).tail(1).values[0], fwSharpe, dwSharpe
    
# Below returns an example rebalancing strategy and its performance relative to no rebalancing
# Below uses BTC/USD, rebalances BTC to be 50% of wealth, rebalances once a week and takes a 0.5% fee everytime it rebalances
# Outputs FW-DW Returns (ie Rebalcing outperformance on final date), FW sharpe ratio, DW sharpe ratio
# Sharpe ratio may be seen as the signal/noise ratio of an investment strategy

rebalance(data, 0.5, 1, 7, 0.005, 'pct')

#Explore different weightings and rebalances frequencies for maximum performance

X = []
y = []
performanceList = []
for frequency in [5, 10, 20, 40, 80, 252]:
    for weighting in [0.3, 0.5, 0.7]:
        performanceList.append(rebalance(data, weighting, 1, frequency, 0.005, 'pct')[0])
        X.append(frequency)
        y.append(weighting)
        
#And plot with the following
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(X, y, performanceList)
plt.show()

#Which suggests historically, optimal BTC/USD portfolio performance came with a 70% allocation and rebalanced once a year
