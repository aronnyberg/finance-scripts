import pandas as pd
from yahoo_fin import stock_info
import numpy as np

#download IWN portfolio constituents at https://www.ishares.com/us/products/239712/ishares-russell-2000-value-etf/1467271812596.ajax?fileType=csv&fileName=IWN_holdings&dataType=fund
iwn_names = pd.read_csv(r'C:\Users\nyber\Documents\IWN_holdings.csv', header=10)
iwn_tickers = iwn_names['Ticker']
iwn_tickers_400 = iwn_tickers[:400]

#Sorting number notation, ie $1.2B to read as the number
def change_nums(i):
    m = {'K': 3, 'M': 6, 'B': 9, 'T': 12}
    return int(float(i[:-1]) * 10 ** m[i[-1]])
#Below uses yahoo_fin API, a simple scrape of the yahoo finance quote table for each stock. My previous version of this code
#computed shares outstanding and other balance sheet measures directly, since then yahoo finance has started charging for blance sheet data
alist = []
for i in iwn_tickers_400:
    try:
        name_dic = {'Ticker':i}
        x = stock_info.get_quote_table(i)
        dic2 = dict(name_dic, **x)
        alist.append(dic2)    
    except:
        pass
      
 df = pd.DataFrame(alist)
#Below sorts aforementioned market cap fix
alist2 = []
for i in df['Market Cap']:
    try:
        alist2.append(change_nums(i))
    except:
        alist2.append(np.nan)
        
df2 = pd.concat([df, pd.DataFrame(alist2, columns=['Market Cap 2'])], axis=1)

#The following reads a pickle database of 3 years of data for all 1,000 IWN stocks, safe to say it'll take a while,
#This code will be in my repository, under Getting Data pt. 1
stock_prices = pd.read_pickle('iwn_2016to05092019_Clean.pkl')
stock_prices = stock_prices.round(1)
stock_price_pct = stock_prices.pct_change(252)

#Following finds 1,2 and 3 year IWN returns and concats them into the main dataframe
alist3yr = []
alist2yr = []
alist1yr = []
n3 = 756
n2 = 504
n1 = 252
for i in iwn_tickers_400:
    try:
        alist3yr.append({'Ticker':i, 'Price3yr':stock_prices[i][n3-22]})
    except:
        alist3yr.append({'Ticker':i, 'Price3yr':np.nan})
    try:   
        alist2yr.append({'Ticker':i, 'Price2yr':stock_prices[i][n2-22]})
    except:
        alist2yr.append({'Ticker':i, 'Price2yr':np.nan})
    try:
        alist1yr.append({'Ticker':i, 'Price1yr':stock_prices[i][n1-22]})
    except:
        alist1yr.append({'Ticker':i, 'Price1yr':np.nan})
        
df_3yr = pd.DataFrame(alist3yr)
df_2yr = pd.DataFrame(alist2yr)
df_1yr = pd.DataFrame(alist1yr)
prev_price_df = pd.concat([df_3yr, df_2yr, df_1yr], axis=1)

prev_price_df = prev_price_df.iloc[:,[0,1,3,5]]

prev_price_df = prev_price_df.set_index('Ticker')
df2 = df2.set_index('Ticker')

df3 = pd.concat([prev_price_df, df2], axis=1)

df3['3yr % Change'] = (df3['Quote Price'] - df3['Price3yr'])/df3['Price3yr']
df3['2yr % Change'] = (df3['Quote Price'] - df3['Price2yr'])/df3['Price2yr']
df3['1yr % Change'] = (df3['Quote Price'] - df3['Price1yr'])/df3['Price1yr']

#Aprroximation for shares outstanding
df3['Shares Out'] = df3['Market Cap 2'] /df3['Quote Price']

#Uses original ishares IWN csv to include some more useful info
iwn_data = iwn_names[['Ticker', 'Weight (%)', 'Sector']]
iwn_data = iwn_data.set_index('Ticker')
df4 = pd.concat([df3, iwn_data],axis=1, join='inner')

# Sorts the stock price range info to be useful, used as a proxy for volatility in analysis
def get_range(i):
    x = (float(str(df4['52 Week Range'].loc[i]).split('-')[0])) 
    y = (float(str(df4['52 Week Range'].loc[i]).split('-')[1]))
    return (y - x)/x
#Applies stock price range sort
iwn_ranges4 = []
for i in iwn_tickers_400:
    try:
        iwn_ranges4.append({'Ticker':i, 'Range':get_range(i)})
    except:
        iwn_ranges4.append({'Ticker':i, 'Range':np.nan})
        
rangedf = pd.DataFrame(iwn_ranges4)
rangedf = rangedf.set_index('Ticker')
df5 = pd.concat([df4, rangedf], axis=1)

#And done, puts it in a pickle
df5.to_pickle('IWN_400_Data.pkl')
