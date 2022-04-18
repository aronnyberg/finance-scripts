import pandas as pd
from getting_daily_yahoo_data import get_daily_data
from dfDataCleaning import cleanDFdailyYahooStockPrices
from sqlalchemy import create_engine
import pymysql
from config import sqlPath

sqlPath = sqlPath+'stockData'

def pulldatatoSQL(numberOfStocks, sqlPath, indexList):
    if indexList == 'IWN':
        stock_names = pd.read_csv('https://www.ishares.com/us/products/239712/ishares-russell-2000-value-etf/1467271812596.ajax?fileType=csv&fileName=IWN_holdings&dataType=fund',header=8)
        # Checked the number of rows below the last stock is bottomRows, which we don't need
        bottomRows = 6
        indexAttribution = ''
    if indexList == 'UKsmallCaps':
        stock_names = pd.read_csv('https://www.ishares.com/us/products/239691/ishares-msci-united-kingdom-smallcap-etf/1467271812596.ajax?fileType=csv&fileName=EWUS_holdings&dataType=fund', header=8)
        #.L specifies London listing, which we need to do for UK stocks
        indexAttribution = '.L'
        bottomRows = 11
    else:
        pass
    # For a local mySQL using pymysql as the database connector, with a schema 'stockData'
    # basic syntax is #engine = create_engine("mysql://user:PASSWORD@localhost/DATABASENAME",echo = True)
    engine_string = sqlPath
    engine = create_engine(engine_string,echo = True)
    connection = engine.connect()

    #last 5 rows useless
    tickers = stock_names.reset_index().iloc[:,0]
    tickers = tickers[1:-bottomRows]
    tickers = tickers+indexAttribution

    # returns full df
    df = get_daily_data(tickers[:numberOfStocks])
    df = cleanDFdailyYahooStockPrices(df)

    df.to_sql('dailyPrices', connection, if_exists='replace')
    
pulldatatoSQL(5, sqlPath, 'UKsmallCaps')


    

    
