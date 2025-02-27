import yfinance as yf
from time_util import ChunkManager
from time_util import Timestamp
import operator
import csv
from memory_util import HardDrive

class TickerInfo:
    def __init__(self):
        pass
    def get_single_ticker_history(self,ticker):
        dat =yf.Ticker(ticker)
        stock_history_dict = dat.history(period='12mo')
        self.print_single_ticker_rpt(stock_history_dict)
    def get_single_ticker_info_complete(self, ticker):
        dat = yf.Ticker(ticker)
        stock_info_dict=dat.info
        self.print_single_ticker_rpt(stock_info_dict)
        
    def get_single_ticker_info_slim(self, ticker):
        try:
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
            return stock_info_slim_dict
        except Exception as e:
            stock_info_slim_dict = {}
            stock_info_slim_dict['symbol'] = ticker
            stock_info_slim_dict['Trouble Extracting'] = str(e)
            return stock_info_slim_dict

    
    def get_info_from_ticker_list(self, ticker_list):
        list = []
        chunk_manager = ChunkManager(150,60,ticker_list)
        for ticker in ticker_list:
            chunk_manager.tally_click()
            slim_dict = self.get_single_ticker_info_slim(ticker)
            list.append(slim_dict)
        return list
    
    def no_or_low_dividend_filter(self, list_of_slim_dicts):
        filtered_list = []
        for slim_dict in list_of_slim_dicts:
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
     
class ExtractTickersFromCsv:
    def __init__(self, nasdaq_file, nyse_file):
        self.nasdaq = []
        self.nyse = []
        self.nasdaq_and_nyse = []
        
        try:
            with open(nasdaq_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                self.nasdaq = [row[0].strip() for row in reader]
        except Exception as e:
            print(e)
            
        try:
            with open(nyse_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                self.nyse = [row[0].strip() for row in reader]
        except Exception as e:
            print(e)
        
        self.nasdaq_and_nyse = self.nasdaq + self.nyse
        HardDrive().save(self.nasdaq_and_nyse, 'exctractedTickers.json')
       
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