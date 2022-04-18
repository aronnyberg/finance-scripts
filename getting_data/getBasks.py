import ccxt
import pandas as pd
from datetime import datetime
import time
import yahoo_fin
from config import sqlPath
from config import sqlPassword
from sqlalchemy import create_engine
import pymysql

binance = ccxt.binance () 
binance.load_markets ()
ftx = ccxt.ftx () 
ftx.load_markets ()
gemini = ccxt.gemini ()
gemini.load_markets ()
kraken = ccxt.kraken () 
kraken.load_markets ()
bitfinex = ccxt.bitfinex ()
bitfinex.load_markets ()
bitstamp = ccxt.bitstamp () 
bitstamp.load_markets ()

def get_basks(thepair, theexchange):
    basks = theexchange.fetch_ticker(thepair)
    bask_dict['bid'].append(basks['bid'])
    bask_dict['ask'].append(basks['ask'])
    bask_dict['asset'].append(basks['symbol'])
    bask_dict['exchange'].append(str(theexchange).upper())
    bask_dict['base'].append(base)

data = pd.read_csv('/Users/aronnyberg/Downloads/crypto200 - Sheet1.csv')
#assets = pd.DataFrame(data)
assetList = data.iloc[:,2].values
#following gives list of symbols
assetList = [i for i in assetList][:5]

bask_dict = {'bid':[], 'ask':[], 'asset':[], 'exchange':[], 'base':[]}
for each in assetList[:]:
  for base in ['USD', 'GBP', 'EUR', 'JPY', 'ETH']:
    try:
      ticker = each+'/'+base
    except:
      ticker = base+'/'+each
    else:
      pass
    for exch in [binance, ftx, gemini, kraken, bitstamp, bitfinex]:
      try:
        get_basks(ticker, exch)
      except:
          pass
  time.sleep(0.5)

#gives df with columns bid, ask, asset, exchange
data = pd.DataFrame(bask_dict)

from yahoo_fin.stock_info import get_live_price

currencyLookUp = {'GBP':[], 'EUR':[], 'JPY':[], 'ETH':[]}
for each in currencyLookUp.keys():
    try:
        #grab data for USD conversion
        #rate = get data for exchange value
        ticker = each+'USD=X'
        rate = get_live_price(ticker)
        #data['base']
        #singleCurrency = data[data['base'] == each]
    except AssertionError:
        pass
        #ETH error, grab ETH data
    except:
        pass
    #transform = 1/rate
    #currencyLookUp.update({each:transform})
    currencyLookUp.update({each:rate})

#Look up and multiply bid,asks by currencyLookUp dict
data['ask'] *= data['base'].map(currencyLookUp).fillna(1)
data['bid'] *= data['base'].map(currencyLookUp).fillna(1)

import time
data['timestamp'] = time.time()

df = data.groupby(['asset','exchange']).ask.mean().unstack().T

longExchange = []
shortExchange = []
longPrice = []
shortPrice = []
asset = []

for each in df.columns:
    max = df[each].max(axis=0)
    min = df[each].min(axis=0)
    pc = (max-min)/min
    maxExchange = df.index[df[each]==max][0]
    minExchange = df.index[df[each]==min][0]
    if  pc > 0.001:
        print(each)
        print(pc)
        longExchange.append(minExchange)
        shortExchange.append(maxExchange)
        longPrice.append(min)
        shortPrice.append(max)
        asset.append(each)

sqlPath = sqlPath+'cryptoData'
engine_string = sqlPath
engine = create_engine(engine_string,echo = True)
connection = engine.connect()

data['timestamp'] = time.time()
data.to_sql('basks', connection, if_exists='replace')
pd.DataFrame({'Long Exchange':longExchange, 'Short Exchange':shortExchange, 
    'Long Price':longPrice, 'Short Price':shortPrice,
          'Asset':asset, 'timestamp': time.time()}).to_sql('arbs', connection, if_exists='replace')

