import pandas_datareader.data as web
import datetime
start = datetime.datetime(2015, 6, 1)
end = datetime.datetime(2016, 7, 5)
#aapl = web.DataReader('AAPL', 'yahoo', start, end)
#aapl.to_csv('aapl.csv')

#sz_399300 = web.DataReader('399300.SZ', 'yahoo', start, end)
#sz_399300.to_csv('sz_399300.csv')

ss_510300 = web.DataReader('510300.SS', 'yahoo', start)
ss_510300.to_csv('ss_510300.csv')