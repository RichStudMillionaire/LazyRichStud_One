# LAZY RICH STUD VERSION 1.0
# OBJECTS AND CLASSES
import csv
import yfinance as yf
import datetime
import time
import os

class LogManager:
    def __init__(self, file_name):
        self.file_name = file_name
    
    def create_log_file(self):
        with open(self.file_name, "w") as file:
            file.write(self.file_name)
            file.write("\n")
            
    def new_paragraph(self, paragraph):
        with open(self.file_name, "a") as file:
            file.write(paragraph)
            file.write("\n")
    
            
    def delete(self, file_name):
        os.remove(file_name)
        
        

class TimeManager:
    def __init__(self):
        pass
    
    def get_datetime_from_epoch(self,epoch):
        return datetime.datetime.fromtimestamp(epoch)
    
    def get_today_in_datetime(self):
        return datetime.datetime.now()
    
    def make_unix_epoch_readable(self,epoch):
        return datetime.datetime.fromtimestamp(epoch).strftime('%m-%d-%Y')
    
    def get_today_in_epoch(self):
        today = datetime.date.today()
        epoch = time.mktime(today.timetuple())
        return epoch
    
    def get_how_long_since_from_epoch(self,epoch_older):
        today = self.get_today_in_datetime()
        older_datetime = self.get_datetime_from_epoch(epoch_older)

        return today-older_datetime
        

class TickerExtractor:
    def __init__(self, csv_file, stock_exchange):
        self.csv = csv_file
        self.ticker_list=[]
        self.stock_exchange = stock_exchange
        self.nasdaq_tickers=['Nasdaq tickers list is empty, load a list from csv file']
        self.nyse_tickers = ['NYSE tickers list is empty at the moment, load a list from csv file']
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
        self.stock_info={}
        
    def get_info_single_ticker(self, ticker):
        dat = yf.Ticker(ticker)
        self.stock_info=dat.info
        return self.stock_info
    
    def stock_pays_dividends_bool(self,ticker):
        info = self.get_info_single_ticker(ticker)
        pays_dividends = False
        
        try:
            info['lastDividendDate']
            pays_dividends=True
            return pays_dividends
            
        except: 
            return pays_dividends
            
            
    
    
    def stock_data_console_rpt(self, data_dictionary):
        for keys in data_dictionary:
            print('{} : {}'.format(keys, data_dictionary[keys]))
    
    def analyse_fifty_two_week_low(self, ticker, max_gap=None):
        info=self.get_info_single_ticker(ticker)
        fifty_two_week_low = info['fiftyTwoWeekLow']
        day_high = info['dayHigh']
        gap = (day_high-fifty_two_week_low)/fifty_two_week_low*100
        
        if (max_gap==None):
            fifty_two_week_low_dict = {"Ticker":ticker, "Analysis": "52-Week-Low", "Day High":day_high, "52-Week-Low":fifty_two_week_low, "Gap":gap, "Max Gap Filter": 'No Gap Filter'}
            return fifty_two_week_low_dict
        elif(gap <= max_gap):
            fifty_two_week_low_dict = {"Ticker":ticker, "Analysis": "52-Week-Low", "Day High":day_high, "52-Week-Low":fifty_two_week_low, "Gap":gap, "Max Gap Filter": max_gap}
            return fifty_two_week_low_dict
        
    def analyse_fifty_day_ma(self, ticker, max_gap=None):
        info=self.get_info_single_ticker(ticker)
        fifty_day_ma = info['fiftyDayAverage']
        day_high = info['dayHigh']
        gap = (day_high-fifty_day_ma)/fifty_day_ma*100
        
        if (max_gap==None):
            fifty_day_ma_dict = {"Ticker":ticker, "Analysis": "50-Day Moving Average", "Day High":day_high, "50-Day Moving Average":fifty_day_ma, "Gap":gap, "Max Gap Filter": 'No Gap Filter'}
            return fifty_day_ma_dict
        elif (gap <= max_gap):
            fifty_day_ma_dict = {"Ticker":ticker, "Analysis": "50-Day Moving Average", "Day High":day_high, "50-Day Moving Average":fifty_day_ma, "Gap":gap, "Max Gap Filter": max_gap}
            return fifty_day_ma_dict
        
    def analyse_two_hundred_day_ma(self, ticker, max_gap=None):
        info=self.get_info_single_ticker(ticker)
        two_hundred_day_ma = info['twoHundredDayAverage']
        day_high = info['dayHigh']
        gap = (day_high-two_hundred_day_ma)/two_hundred_day_ma*100
        
        if (max_gap==None):
            fifty_day_ma_dict = {"Ticker":ticker, "Analysis": "200-Day Moving Average", "Day High":day_high, "200-Day Moving Average":two_hundred_day_ma, "Gap":gap, "Max Gap Filter": 'No Gap Filter'}
            return fifty_day_ma_dict
        elif (gap <= max_gap):
            fifty_day_ma_dict = {"Ticker":ticker, "Analysis": "200-Day Moving Average", "Day High":day_high, "200-Day Moving Average":two_hundred_day_ma, "Gap":gap, "Max Gap Filter": max_gap}
            return fifty_day_ma_dict
            
        
        
    
            
        
    
        
        
    
    
         
        
    
        
        