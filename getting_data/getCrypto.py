import ccxt
import pandas as pd
import time
import matplotlib.pyplot as plt
import datetime

#coinbase = ccxt.coinbase()
#coinbase.load_markets()
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

def get_candles(theasset, theexchange):
    candles = theexchange.fetch_ohlcv(theasset, '1d')
    #incredibly inefficent but hey ho
    for candle in candles:
        adict['asset'].append(candle['thepair'])
        adict['exchange'].append(str(theexchange).upper())
        adict['dates'].append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f'))
        adict['open'].append(candle[1])
        adict['high'].append(candle[2])
        adict['low'].append(candle[3])
        adict['close'].append(candle[4])

adict = {'dates':[], 'close':[], 'open':[], 'high':[], 'low':[], 'asset':[], 'exchange':[]}

for each in ['ETH']:
    for base in ['USD', 'USDT', 'TUSD','GBP', 'EUR', 'JPY', 'ETH']:
        for exch in [binance, ftx, gemini, kraken, bitstamp, bitfinex]:
            try:
                print(ticker)
                ticker = each+'/'+base
                get_candles(ticker, exch)
            except:
                pass
            #except:
            #    ticker = base+'/'+each
            #    get_candles(ticker, exch)
            time.sleep(0.5)

data = pd.DataFrame(adict)

print(data)

plt.figure()
plt.plot(data)
plt.show()





