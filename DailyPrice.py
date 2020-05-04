

#2020-4-24
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import pandas as pd

class stock_price():
    def __init__(self,start,end):
        self.symbol=[]
        self.start=start
        self.end=end   
        self.data_dir='historical_data/'
    
    def get_stock_list(self):
        with open(self.data_dir + 'StockList.txt') as f:
            self.symbol = [line.rstrip() for line in f]  
        f.close()
        print(self.symbol)

    def save_historical_price_csv(self):
        for sym in self.symbol:
            try:
                #histDF = data.DataReader(sym, 'yahoo', self.start, self.end)
                histDF = pdr.get_data_yahoo(sym, start=self.start, end=self.end)
                histDF['Symbol']=sym
                histDF.to_csv(self.data_dir + sym + '.csv')
            except Exception:
                print(sym + ' cannot be loaded!')
    
    def extract_close_price2(self):
        stocks=[]
        for sym in self.symbol:
            stocks.append(pd.read_csv(self.data_dir + sym + '.csv', usecols=['Symbol', 'Date', 'Adj Close']))
        close_price=pd.concat(stocks).pivot(index='Date', columns='Symbol', values='Adj Close')
        #print(close_price)
        close_price.to_csv(self.data_dir + 'focused_price.csv')

    def extract_close_price(self):
        def stock(sym):
            return (pdr.get_data_yahoo(sym, start=self.start, end=self.end))
        stocks = map (stock, self.symbol)
        close_price=pd.concat(stocks, keys=self.symbol, names=['Symbol', 'Date'])
        print(close_price)
        daily_close_px = close_price[['Adj Close']].reset_index().pivot('Date', 'Symbol', 'Adj Close')
        #print(daily_close_px)
        daily_close_px.to_csv(self.data_dir + 'focused_price.csv')


s=stock_price('2020-03-01','2020-04-30')
s.get_stock_list()
s.save_historical_price_csv()
s.extract_close_price2()
#print(close_price)
