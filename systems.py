from yf_api import Filter
from yf_api import InfoExtractor
import yfinance as yf
import json
import os
from datetime import datetime
import csv
import time

class TickerInfo:
    def __init__(self):
        pass
    def get_single_ticker_info_complete(self, ticker):
        dat = yf.Ticker(ticker)
        stock_info_dict=dat.info
        self.print_single_ticker_rpt(stock_info_dict)
        
    def get_single_ticker_info_slim(self, ticker):
        dat = yf.Ticker(ticker)
        info=dat.info
        keys_to_keep = ['symbol', 'dayHigh', 'fiftyDayAverage', 'twoHundredDayAverage', 'targetHighPrice', 'targetLowPrice', 'targetMedianPrice', 'fiftyTwoWeekLow', 'dividendYield', 'payoutRatio', 'fiveYearAverageYield', 'lastDividendValue','lastDividendDate']
        stock_info_slim_dict = {key: info[key] for key in keys_to_keep if key in info}
        key_to_verify_dividend = 'dividendYield'
        if key_to_verify_dividend in stock_info_slim_dict:
            stock_info_slim_dict["stockPaysDividends"] = True
            if stock_info_slim_dict['dividendYield'] > 0.05:
                stock_info_slim_dict['stockPaysHighDividends'] = True
            elif stock_info_slim_dict['dividendYield'] < 0.01:
                stock_info_slim_dict['stockPaysLowDividends'] = True
            
        else:
            stock_info_slim_dict['stockPaysDividends'] = False
        self.print_single_ticker_rpt(stock_info_slim_dict)
        return stock_info_slim_dict
    
    def get_info_from_ticker_list(self, ticker_list):
        list = []
        chunk_manager = ChunkManager(150,60,ticker_list)
        for ticker in ticker_list:
            chunk_manager.tally_click()
            list.append(self.get_single_ticker_info_slim(ticker))
        return list
    
    def no_or_low_dividend_filter(self, list_of_slim_dicts):
        filtered_list = []
        for slim_dict in list_of_slim_dicts:
            print(slim_dict)
            if slim_dict['stockPaysDividends'] == False:
                filtered_list.append(slim_dict)
            elif 'stockPaysLowDividends' in slim_dict and slim_dict['stockPaysLowDividends'] == True:
                filtered_list.append(slim_dict)
        return filtered_list
    
    def below_fifty_day_moving_average_filter(self, list_of_slim_dicts, gap):
        filtered_list = []
        for slim_dict in list_of_slim_dicts:
            if 'dayHigh' in slim_dict:
                day_high = slim_dict['dayHigh']
                ma = slim_dict['fiftyDayAverage']
                real_gap = (ma-day_high)/ma*100
                if slim_dict['dayHigh'] < slim_dict['fiftyDayAverage'] and real_gap >= gap:
                    filtered_list.append(slim_dict)
        return filtered_list 
    
    def below_median_price_target_filter(self, list_of_slim_dicts,gap):
        filtered_list=[]
        for slim_dict in list_of_slim_dicts:
            if 'targetMedianPrice' in slim_dict and 'dayHigh' in slim_dict:
                day_high = slim_dict['dayHigh']
                median_target = slim_dict['targetMedianPrice']
                real_gap = (median_target-day_high)/median_target*100
                if day_high < median_target and real_gap >= gap:
                    filtered_list.append(slim_dict)
        return filtered_list
    
    def no_penny_stocks_filter(self, list_of_slim_dicts, min_stock_price):
        filtered_list = []
        for slim_dict in list_of_slim_dicts:
            if 'dayHigh' in slim_dict:
                if slim_dict['dayHigh'] >= min_stock_price:
                    filtered_list.append(slim_dict)
        return filtered_list
                
    
    def get_str_from_dict(self, list_of_dict):
        list = []
        for dictionary in list_of_dict:
            list.append(dictionary['symbol'])      
        return list
        
    def print_single_ticker_rpt(self, ticker_info):
        print("Date and time of the report : {}".format(Timestamp().now()))
        print()
        for key, value in ticker_info.items():
            print("{} : {}".format(key,value))
        print()
        

class HardDrive:
    def __init__(self):
        self.list = {}
        self.json_string = ""
        
        
    def convert_dict_to_json_string(self):
        self.json_string = json.dumps(self.dict)
        
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
        except Exception as e:
            print(e)
            return False
        
    def format(self, file_name):
        try:
            os.remove(file_name)
        except Exception as e:
            print(e)
            
class Timestamp:
    def __init__(self):
        pass
    def now(self):
        return datetime.now()
    
class ChunkManager:
    def __init__(self, chunk_size, pause_time_in_seconds, ticker_list):
        self.chunk_size = chunk_size
        self.pause = pause_time_in_seconds
        self.list_length = len(ticker_list)
        self.total = 0
        self.count=0
    def tally_click(self):
        self.count+=1
        self.check_tally_and_pause()
    def check_tally_and_pause(self):
        if self.count == self.chunk_size:
            self.total+=self.count
            print("Zzz... Going to sleep for {} seconds".format(self.pause))
            print("Progress : {} tickers out of {}".format(self.total, self.list_length))
            time.sleep(self.pause)
            self.count = 0
            
            
    
class ExtractTickersFromCsv:
    def __init__(self, nasdaq_file, nyse_file):
        self.nasdaq = []
        self.nyse = []
        self.nasdaq_and_nyse = []
        
        try:
            with open(nasdaq_file, 'r') as file:
                reader = csv.reader(file)
                self.nasdaq = [row[0].strip() for row in reader]
        except Exception as e:
            print(e)
            
        try:
            with open(nyse_file, 'r') as file:
                reader = csv.reader(file)
                self.nyse = [row[0].strip() for row in reader]
        except Exception as e:
            print(e)
        
        self.nasdaq_and_nyse = self.nasdaq + self.nyse
        
    def get_nasdaq(self):
        return self.nasdaq
    def get_nyse(self):
        return self.nyse
    def get_nasdaq_plus_nyse(self):
        return self.nasdaq_and_nyse
    def print_rpt(self):
        print("NASDAQ : {}".format(len(self.nasdaq)))
        print(self.nasdaq)
        print("NYSE : {}".format(len(self.nyse)))
        print(self.nyse)
        print("NASDAQ + NYSE")
        print("Actual : {}".format(len(self.nasdaq_and_nyse)))
        print("Expected : {}".format(len(self.nasdaq)+len(self.nyse)))
        print(self.nasdaq_and_nyse)
        
        
class GrowthSystem:
    def __init__(self):
        self.hard_drive = HardDrive()
        self.info = TickerInfo()
        self.nasdaq = []
        self.nyse = []
        self.nasdaq_and_nyse = []
        self.booth()
    def booth(self):
        self.check_for_active_session()
    def check_for_active_session(self):
        self.session=self.hard_drive.load("ActiveSession.json")
        if self.session == False:
            print("No active session : Starting a new session, please wait")
            self.start_new_session()
        else:
            pass
    def start_new_session(self):
        tickers = ExtractTickersFromCsv("nasdaq.csv","nyse.csv")
        self.nasdaq = tickers.get_nasdaq()
        self.nyse = tickers.get_nyse()
        self.nasdaq_and_nyse = tickers.get_nasdaq_plus_nyse()
        self.hard_drive.save(self.nasdaq, "SessionNasdaq.json")
        self.hard_drive.save(self.nyse, "SessionNyse.json")
        self.hard_drive.save(self.nasdaq_and_nyse, "SessionNasdaqAndNyse.json")
        self.collect_ticker_info(self.nasdaq_and_nyse)
    def collect_ticker_info(self, ticker_list):

        info_list=self.info.get_info_from_ticker_list(ticker_list)
        self.hard_drive.save(info_list, "ActiveSession.json")
    def restore_session(self):
        self.session=self.hard_drive.load('ActiveSession.json')
        self.filtered_info_one=self.info.no_or_low_dividend_filter(self.session)
        self.hard_drive.save(self.filtered_info_one,'filterOneDividend.json')
        self.filtered_info_two = self.info.below_fifty_day_moving_average_filter(self.filtered_info_one,20)
        print(len(self.filtered_info_two))
        self.filtered_info_three = self.info.below_median_price_target_filter(self.filtered_info_two,20)
        print(len(self.filtered_info_three))
        self.filtered_info_four = self.info.no_penny_stocks_filter(self.filtered_info_three, 5)
        self.filtered_ticker_list = self.info.get_str_from_dict(self.filtered_info_four)
        print(self.filtered_ticker_list)
        self.hard_drive.save(self.filtered_ticker_list, 'growthWinners.json')
        
        
        
        
        
        
        
        