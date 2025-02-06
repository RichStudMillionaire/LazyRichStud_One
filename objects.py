# LAZY RICH STUD VERSION 1.0
# OBJECTS AND CLASSES
import csv
import yfinance as yf
import datetime
import time
import os
import json

class TallyCounter:
    def __init__(self):
        self.count = 0
    def click(self):
        self.count+=1
    def reset(self):
        self.count = 0

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
        self.tally = TallyCounter()
        self.dividend_filtered_dict={}
        
    def get_info_single_ticker(self, ticker):
        try:
            dat = yf.Ticker(ticker)
            self.stock_info=dat.info
            return self.stock_info
        except Exception as e: 
            print("Couldn't extract info from {}\n{}".format(ticker,e))
            self.long_pause(300)
    
    def stock_pays_dividends_bool(self,ticker):
        info = self.get_info_single_ticker(ticker)
        pays_dividends = False
        
        try:
            info['lastDividendDate']
            pays_dividends=True
            return pays_dividends
            
        except: 
            return pays_dividends
    
    def long_pause(self, pause_seconds):
        print("Zzz... Long Pause")
        time.sleep(pause_seconds)
            
    def pause_info_extraction(self, pause_rate):
        self.tally.click()
        if self.tally.count == pause_rate:
            print("Zzzzz Sleeping")
            time.sleep(60)
            self.tally.reset()
            
    def filter_ticker_list_on_dividends(self, ticker_list, chunk_size, return_dividend_stocks = True):
        self.dividend_tickers = []
        self.no_dividend_tickers = []
        self.return_dividends = return_dividend_stocks
        
        for ticker in ticker_list:
            self.pause_info_extraction(chunk_size)
            bool=self.stock_pays_dividends_bool(ticker)
            if bool:        
                self.dividend_tickers.append(ticker)
            else:
                self.no_dividend_tickers.append(ticker)

        if self.return_dividends:
            return self.dividend_tickers
        else:
            return self.no_dividend_tickers
        
    def filter_fifty_ma(self, ticker_list, ma_gap, chunk_size):
        for ticker in ticker_list:
            self.pause_info_extraction(chunk_size)
            info=self.get_info_single_ticker(ticker)
            fifty_ma = info['fiftyDayAverage']
            day_high = info['dayHigh']
            
            if (day_high >= fifty_ma):
                pass
            else:
                gap = (fifty_ma - day_high)/fifty_ma*100 
                if gap < ma_gap:
                    return ticker

                        
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
        
    def analyse_fifty_day_ma(self, ticker, below_ma_gap=None):
        info=self.get_info_single_ticker(ticker)
        fifty_ma = info['fiftyDayAverage']
        day_high = info['dayHigh']
        self.analyse_fifty_ma_dict ={}
        
        if (day_high >= fifty_ma):
            pass
        else:
            gap = (fifty_ma - day_high)/fifty_ma*100 
            if below_ma_gap!=None:
                if gap < below_ma_gap:
                    self.analyse_fifty_ma_dict["symbol"]=ticker
                    self.analyse_fifty_ma_dict["fiftyDayAverage"]=fifty_ma
                    self.analyse_fifty_ma_dict["dayHigh"]=day_high
                    self.analyse_fifty_ma_dict["fiftyDayAverageGap"] = gap
                    
            else:   
                self.analyse_fifty_ma_dict["symbol"]=ticker
                self.analyse_fifty_ma_dict["fiftyDayAverage"]=fifty_ma
                self.analyse_fifty_ma_dict["dayHigh"]=day_high
                self.analyse_fifty_ma_dict["fiftyDayAverageGap"] = below_ma_gap
                
        return self.analyse_fifty_ma_dict
                
    def filter_fifty_day_ma(self, ticker, below_ma_gap=None):
        pass
                    
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
        
    def analyse_price_target(self):
        pass
        
    def flag_two_hundred_ma(self):
        pass
    
    def flag_fifty_two_week_low(self):
        pass
        
class HardDrive:
    def __init__(self):
        self.dict = {}
        self.json_string = ""
        
        
    def convert_dict_to_json_string(self):
        self.json_string = json.dumps(self.dict, indent=1)
        
    def save(self, dict, file_name):
        self.dict = dict
        self.convert_dict_to_json_string()
        
        with open(file_name, 'w') as file:
            file.write(self.json_string)
            
    def load(self, file_name):
        try:    
            with open(file_name,'r') as file:
                self.dict = json.load(file)
                return self.dict
        except:
            return False
            
            
        
        
            
        
        
    
            
        
    
        
        
    
    
         
        
    
        
        