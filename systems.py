from yf_api import Filter
from yf_api import InfoExtractor
import yfinance as yf
import json
import os
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import csv
import time
import operator

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
        keys_to_keep = ['symbol', 'dayHigh', 'fiftyDayAverage', 'twoHundredDayAverage', 'targetHighPrice', 'targetLowPrice', 'targetMedianPrice', 'fiftyTwoWeekLow', 
                        'dividendYield', 'payoutRatio', 'fiveYearAverageYield', 'lastDividendValue','lastDividendDate', 'trailingEps', 'forwardEps']
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
    
    def high_dividend_filter(self, list_of_slim_dicts):
        filtered_list=[]
        for slim_dict in list_of_slim_dicts:
            if 'stockPaysHighDividends' in slim_dict:
                filtered_list.append(slim_dict)
        return filtered_list
    
    def undervalued_filter(self, list_of_slim_dicts, gap):
        filtered_list = []
        for slim_dict in list_of_slim_dicts:
            if 'targetMedianPrice' in slim_dict:
                price = slim_dict['dayHigh']
                target = slim_dict['targetMedianPrice']
                real_gap = (target-price)/target*100
                if price < target and real_gap >= gap:
                    filtered_list.append(slim_dict)
        return filtered_list
                    
    def fifty_two_week_low_filter(self, list_of_slim_dicts, gap):
        filtered_list = []
        for slim_dict in list_of_slim_dicts:
            if 'fiftyTwoWeekLow' in slim_dict:
                day_high = slim_dict['dayHigh']
                low_52 = slim_dict['fiftyTwoWeekLow']
                real_gap = (day_high-low_52)/day_high*100
                slim_dict['fiftyTwoWeekLowGap'] = real_gap
                if real_gap <= gap:
                    filtered_list.append(slim_dict)
        return filtered_list
                
    def below_fifty_day_moving_average_filter(self, list_of_slim_dicts, gap):
        filtered_list = []
        for slim_dict in list_of_slim_dicts:
            if 'dayHigh' in slim_dict:
                day_high = slim_dict['dayHigh']
                ma = slim_dict['fiftyDayAverage']
                real_gap = (ma-day_high)/ma*100
                slim_dict['fiftyDayAverageGap']=real_gap
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
                slim_dict['targetMedianPriceGap'] = real_gap
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
    
    def payout_ratio_filter(self, list_of_slim_dicts):
        filtered_list = []
        for slim_dict in list_of_slim_dicts:
            if 'payoutRatio' in slim_dict:
                if slim_dict['payoutRatio'] < 1:
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
        
    def sort_ascending(self, dict_list, key):
        try:
            sorted_list = sorted(dict_list, key=operator.itemgetter(key))
        except Exception as e:
            print("Could not sort list in ascending order with {} as key : {}".format(key,e))
        return sorted_list
    
    def sort_descending(self, dict_list, key):
        try:
            sorted_list = sorted(dict_list, key=operator.itemgetter(key), reverse=True)
        except Exception as e:
            print("Could not sort list in descending order with {} as key : {}".format(key,e))
        return sorted_list
        
        

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
    def today(self):
        return date.today()
    
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
        
class Salary:
    def __init__(self):
        self.salary = 1
        self.pay_frequency = 'Biweekly'
        self.raise_frequency = 'Monthly'
        self.raise_rate = .25
    def renegociate(self, new_salary):
        self.salary = new_salary
    def set_first_day_of_work(self):
        pass
    def print_compensation_report_current(self):
        pass
    def print_compensation_report_history(self):
        pass

class Ledger:
    def __init__(self):
        self.hard_drive = HardDrive()
        self.gross_revenue = 0
        self.net_revenue = 0
        self.salary_paid = 0
        self.ledger = []
    
    def buy_stock(self, ticker, qty, price):
        ledger_entry = {}
        ledger_entry['symbol'] = ticker
        ledger_entry['transaction'] = 'Buy'
        ledger_entry['qty'] = qty
        ledger_entry['UnitaryBuyingPrice'] = price
        total_cost = qty*price
        ledger_entry['totalCost'] = total_cost
        self.post(ledger_entry,0)
    
    def sell_stock(self, ticker, qty, price):
        ledger_entry = {}
        ledger_entry['symbol'] = ticker
        ledger_entry['transaction'] = 'Sell'
        ledger_entry['qty'] = qty
        ledger_entry['UnitaryBuyingPrice'] = price
        total_cost = qty*price
        ledger_entry['totalCost'] = total_cost
        self.post(ledger_entry,1)
        
    def post(self, ledger_entry, transaction_int):
        self.transaction = []
        self.buy = {}
        self.sell = {}
    
        if transaction_int == 0:
            self.buy = ledger_entry
        elif transaction_int == 1:
            self.sell = ledger_entry
    
    def read(self):
        pass
        

class GrowthSystem:
    def __init__(self):
        self.id = "Growth System"
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
            print("Restoring active session ... Please wait")
            self.restore_session()
    def start_new_session(self):
        tickers = ExtractTickersFromCsv("nasdaq.csv","nyse.csv")
        self.nasdaq = tickers.get_nasdaq()
        self.nyse = tickers.get_nyse()
        self.nasdaq_and_nyse = tickers.get_nasdaq_plus_nyse()
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
        
class DividendSystem:
    def __init__(self):
        self.id = "Dividends System"
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
            print("Restoring active session ... Please wait")
            self.restore_session()
    def start_new_session(self):
        tickers = ExtractTickersFromCsv("nasdaq.csv","nyse.csv")
        self.nasdaq = tickers.get_nasdaq()
        self.nyse = tickers.get_nyse()
        self.nasdaq_and_nyse = tickers.get_nasdaq_plus_nyse()
        self.collect_ticker_info(self.nasdaq_and_nyse)
    def collect_ticker_info(self, ticker_list):
        info_list=self.info.get_info_from_ticker_list(ticker_list)
        self.hard_drive.save(info_list, "ActiveSession.json")
    def restore_session(self):
        self.filtered_list = self.info.high_dividend_filter(self.session)
        self.filtered_list = self.info.fifty_two_week_low_filter(self.filtered_list,5)
        self.filtered_list = self.info.payout_ratio_filter(self.filtered_list)
        self.finalists = self.info.get_str_from_dict(self.filtered_list)
        print(self.finalists)
        
class CustomizableSystem:
    def __init__(self):
        self.id = "Customizable System"
        self.complete_list = []
        self.filtered_list = []
        self.hard_drive = HardDrive()
        self.info = TickerInfo()
        self.nasdaq = []
        self.nyse = []
        self.nasdaq_and_nyse = []
        self.booth()
    def booth(self):
        self.check_for_active_session()
    def check_for_active_session(self):
        self.complete_list=self.hard_drive.load("CustomizableSystem.json")
        if self.complete_list == False:
            print("No active session : Starting a new session, please wait")
            self.start_new_session()
        else:
            print("Restoring active session ... Please wait")
            self.restore_session()
    def start_new_session(self):
        tickers = ExtractTickersFromCsv("nasdaq.csv","nyse.csv")
        self.nasdaq = tickers.get_nasdaq()
        self.nyse = tickers.get_nyse()
        self.nasdaq_and_nyse = tickers.get_nasdaq_plus_nyse()
        self.collect_ticker_info(self.nasdaq_and_nyse)
    def collect_ticker_info(self, ticker_list):
        info_list=self.info.get_info_from_ticker_list(ticker_list)
        self.hard_drive.save(info_list, "CustomizableSystem.json")
    def restore_session(self):
        self.complete_list = self.hard_drive.load('CustomizableSystem.json')
        self.filtered_list = self.complete_list
    def filter_50_day_moving_average(self, gap):
        dict_list = self.filtered_list
        self.filtered_list=self.info.below_fifty_day_moving_average_filter(dict_list, gap)
        return self.filtered_list
    def filter_52_week_low(self, gap):
        dict_list = self.filtered_list
        self.filtered_list=self.info.fifty_two_week_low_filter(dict_list, gap)
        return self.filtered_list
    def filter_below_price_target(self, gap):
        dict_list = self.filtered_list
        self.filtered_list = self.info.below_median_price_target_filter(dict_list, gap)
        return self.filtered_list
    def filter_min_stock_price(self, min_price):
        dict_list = self.filtered_list
        self.filtered_list = self.info.no_penny_stocks_filter(dict_list, min_price)
        return self.filtered_list
    def filter_payout_ratio(self):
        dict_list = self.filtered_list
        self.filtered_list = self.info.payout_ratio_filter(dict_list)
        return self.filtered_list
    def filter_low_or_no_dividends(self):
        dict_list = self.filtered_list
        self.filtered_list = self.info.no_or_low_dividend_filter(dict_list)
        return self.filtered_list
    def filter_high_dividends(self):
        dict_list = self.filtered_list
        self.filtered_list = self.info.high_dividend_filter(dict_list)
        return self.filtered_list
        
    def print_finalists_rpt(self):
        print("{} results matching your criteria".format(len(self.filtered_list)))
        print()
        for slim_dict in self.filtered_list:
            self.info.print_single_ticker_rpt(slim_dict)
    def clear_filters(self):
        self.filtered_list = self.complete_list
    
    
        
        
        
        
        
        
        