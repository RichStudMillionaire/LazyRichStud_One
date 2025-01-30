# LAZY RICH STUD VERSION 1.0
# OBJECTS AND CLASSES
import csv
import yfinance as yf

class TickerExtractor:
    def __init__(self, csv_file, stock_exchange):
        self.csv = csv_file
        self.ticker_list={}
        self.stock_exchange = stock_exchange
        self.nasdaq_tickers={'Nasdaq tickers list is empty, load a list from csv file'}
        self.nyse_tickers = {'NYSE tickers list is empty at the moment, load a list from csv file'}
        self.extract_tickers()


    def extract_tickers(self):
        with open(self.csv, 'r') as file:
            reader = csv.reader(file)
            self.ticker_list = [row[0] for row in reader]
            
        if (self.stock_exchange == 'nasdaq'):
            self.nasdaq_tickers = self.ticker_list
        elif (self.stock_exchange == 'nyse'):
            self.nyse_tickers = self.ticker_list
    
    def get_nasdaq_tickers(self):
        return self.nasdaq_tickers
    
    def get_nyse_tickers(self):
        return self.nyse_tickers
    
    def get_nasdaq_list_length(self):
        return len(self.nasdaq_tickers)
    
    def get_nyse_list_length(self):
        return len(self.nyse_tickers)
    
            
        
        
class Bank:
    def __init__(self):
        self.deposit=0
        self.withdrawal=0
        self.cash_and_titles=0
        self.owner_contribution=0
        
    
    def get_owner_contribution(self):
        return '{}$'.format(self.owner_contribution)
    
    def get_cash_and_titles(self):
        return "{}$".format(self.cash_and_titles)
    
    def update_cash_and_titles(self, new_cash_and_titles):
        self.cash_and_titles = new_cash_and_titles
        self.get_roi()
    
    def account_withdrawal(self, amount_withdrawn):
        self.cash_and_titles-=amount_withdrawn
        self.owner_contribution-=amount_withdrawn
        
    def account_deposit(self, amount_deposited):
        self.cash_and_titles+=amount_deposited
        self.owner_contribution+=amount_deposited
        
    def get_roi(self):
        
        try:            
            roi=int((self.get_cash_and_titles()-self.get_owner_contribution())/self.get_cash_and_titles*100)
            return "{}%".format(roi)
        except:
            return 0
        
class StockInfoReader:
    def __init__(self, nasdaq_list = {}, nyse_list = {}):
        self.nasdaq = nasdaq_list
        self.nyse = nyse_list
        
    def get_info_single_ticker(self, ticker):
        dat = yf.Ticker(ticker)
        return dat.info
    
    def stock_data_console_rpt(self, data_dictionary):
        for keys in data_dictionary:
            print('{} : {}'.format(keys, data_dictionary[keys]))
            
    
    
         
        
    
        
        