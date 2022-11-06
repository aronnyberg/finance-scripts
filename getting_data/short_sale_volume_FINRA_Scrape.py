#Following script scrapes short volume data from the FINRA website, for every stock on excahnges NYSE, NASDAQ since the start of 2019.
#for the main exchanges. 
#Simply plug desired dates in American formatto the following function as
# get_finra('10/08/2019', 10/09/2019') for the two day period in October 2019

#This is a replication of the sqzme index published here https://squeezemetrics.com/monitor/dix?
#With the methodology here https://squeezemetrics.com/monitor/download/pdf/short_is_long.pdf
print('a')
import requests
import pandas as pd
import io
from xone import calendar

def get_finra(start_date, end_date):
    def business_dates(start, end):
        us_cal = calendar.USTradingCalendar()
        kw = dict(start=start, end=end)
        return pd.bdate_range(**kw).drop(us_cal.holidays(**kw))
    expiration = business_dates(start_date, end_date)
    mod = expiration.strftime("%Y%m%d")
    stringNASDAQ1 = "http://regsho.finra.org/FNQCshvol20190808.txt"
    stringNASDAQ2 = "http://regsho.finra.org/FNSQshvol20190808.txt"
    stringNYSE = "http://regsho.finra.org/FNYXshvol20190808.txt"

    a = []
    b = []
    c = []
    for i in mod:
        a.append(stringNASDAQ1.replace("20190808", i))
        b.append(stringNASDAQ2.replace("20190808", i))
        c.append(stringNYSE.replace("20190808", i))
        
    duffyNASDAQ1 = []
    for i in a:
        urlt = requests.get(i).content
        new = (pd.read_csv(io.StringIO(urlt.decode('utf-8')), sep="|"))
        duffyNASDAQ1.append(new)
    duffyNASDAQ2 = []
    for i in b:
        urlt = requests.get(i).content
        new = (pd.read_csv(io.StringIO(urlt.decode('utf-8')), sep="|"))
        duffyNASDAQ2.append(new)
    duffyNYSE = []
    for i in c:
        urlt = requests.get(i).content
        new = (pd.read_csv(io.StringIO(urlt.decode('utf-8')), sep="|"))
        duffyNYSE.append(new)
        
    listNASDAQ1 = []
    for i in duffyNASDAQ1:
        listNASDAQ1.append(i)
    dfNASDAQ1 = pd.concat(listNASDAQ1)
    
    listNASDAQ2 = []
    for i in duffyNASDAQ2:
        listNASDAQ2.append(i)
    dfNASDAQ2 = pd.concat(listNASDAQ2)
        
    listNYSE = []
    for i in duffyNYSE:
        listNYSE.append(i)
    dfNYSE = pd.concat(listNYSE)
    
    dfNASDAQ1 = dfNASDAQ1.dropna()
    dfNASDAQ2 = dfNASDAQ2.dropna()
    dfNYSE = dfNYSE.dropna()
    
    formaty = '%Y%m%d'
    
    dfNASDAQ1['DateTime'] = pd.to_datetime(dfNASDAQ1['Date'], format=formaty)
    dfNASDAQ1 = dfNASDAQ1.set_index(dfNASDAQ1['DateTime'])
    dfNASDAQ1_ = dfNASDAQ1[['Symbol', 'ShortVolume', 'TotalVolume']]
    dfNASDAQ1_['DPI'] = dfNASDAQ1_['ShortVolume'] / dfNASDAQ1_['TotalVolume']
    
    dfNASDAQ2['DateTime'] = pd.to_datetime(dfNASDAQ2['Date'], format=formaty)
    dfNASDAQ2 = dfNASDAQ2.set_index(dfNASDAQ2['DateTime'])
    dfNASDAQ2_ = dfNASDAQ2[['Symbol', 'ShortVolume', 'TotalVolume']]
    dfNASDAQ2_['DPI'] = dfNASDAQ2_['ShortVolume'] / dfNASDAQ2_['TotalVolume']
    
    dfNYSE['DateTime'] = pd.to_datetime(dfNYSE['Date'], format=formaty)
    dfNYSE = dfNYSE.set_index(dfNYSE['DateTime'])
    dfNYSE_ = dfNYSE[['Symbol', 'ShortVolume', 'TotalVolume']]
    dfNYSE_['DPI'] = dfNYSE_['ShortVolume'] / dfNYSE_['TotalVolume']
    
    thedf = pd.concat([dfNASDAQ2_, dfNASDAQ1_, dfNYSE_])
    
    thedfsort = thedf.pivot_table(values='DPI', index='Symbol', columns='DateTime')
    
    picklename = 'finra'+mod[0]+'_'+ mod[-1] + '.pkl'
    
    print('working')
    print(thedfsort.head())
    thedfsort.to_pickle(picklename)

get_finra('10/08/2019', '10/09/2019')
