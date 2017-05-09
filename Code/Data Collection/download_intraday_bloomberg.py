import pybbg
from datetime import datetime
from datetime import timedelta
import pandas as pd

# define export file paths
export_path = 'H:/Course Docs/Big Data/Final Project/Data/IntradayPrices/'

# initialize retrieval tool
bbg = pybbg.Pybbg()
bbg.service_refData()
# define tickers and fields to download
tickers = ['AAPL', 'FB', 'TSLA']
fld_list = ['open', 'high', 'low', 'close', 'volume']

# set end date to the day before today
end_date = datetime(datetime.today().year, datetime.today().month, datetime.today().day) + timedelta(days=-1)

# for each ticker
for ticker in tickers:
    # retrieve intraday prices
    df = bbg.bdib(ticker+' US Equity', fld_list, datetime(2017, 3, 1), end_date, eventType='TRADE', interval=1)
    # subtract five hours to adjust the default GMT time back to Eastern Standard Time (EST)
    df.index = [x - pd.to_timedelta(5, unit='h') for x in df.index]
    # write to file
    df[fld_list].to_csv(export_path+'IntradayPrice.'+ticker+'.csv', cols=fld_list, index_label='date')
