import pybbg
from datetime import datetime
from datetime import timedelta
import pandas as pd

export_path = 'H:/Course Docs/Big Data/Final Project/'

bbg = pybbg.Pybbg()
bbg.service_refData()
tickers = ['AAPL', 'FB', 'TWTR', 'TSLA']
fld_list = ['open', 'high', 'low', 'close', 'volume']

end_date = datetime(datetime.today().year, datetime.today().month, datetime.today().day) + timedelta(days=-1)

for ticker in tickers:
    df = bbg.bdib(ticker+' US Equity', fld_list, datetime(2017, 3, 1), end_date, eventType='TRADE', interval=1)
    df.index = [x - pd.to_timedelta(5, unit='h') for x in df.index]
    df[fld_list].to_csv(export_path+'IntradayPrice.'+ticker+'.csv', cols=fld_list, index_label='date')
