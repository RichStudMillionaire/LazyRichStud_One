from memory_util import HardDrive
from stock_info_util import ExtractTickersFromCsv
from stock_info_util import TickerInfo
from reports_util import Report


  
class GrowthSystem:
    def __init__(self):
        self.report = Report()
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
        self.filtered_info=self.hard_drive.load('ActiveSession.json')
        self.filtered_info=self.info.no_or_low_dividend_filter(self.filtered_info)
        self.filtered_info= self.info.below_fifty_day_moving_average_filter(self.filtered_info,20)
        self.filtered_info= self.info.below_median_price_target_filter(self.filtered_info,20)
        self.filtered_info = self.info.no_penny_stocks_filter(self.filtered_info, 20)
        self.filtered_info = self.info.uptrend_filter(self.filtered_info)
        print(len(self.filtered_info))
        self.inDepthAnalysis()
        
    def inDepthAnalysis(self):
        self.filtered_ticker_list = self.info.get_str_from_dict(self.filtered_info)
        self.report.add_system_winners_to_report(self.filtered_ticker_list)
        
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
        self.finalists = self.filtered_list
        self.final_list = self.info.get_str_from_dict(self.finalists)  
        self.deep_analysis()
    def deep_analysis(self):
        #print(self.final_list)
        #print()
        #print('Highest Dividend')
        highest_dividend = self.info.sort_descending(self.filtered_list, 'dividendYield')
    
        print(self.info.print_multiple_ticker_rpts(highest_dividend))      

        
        
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
    
    
        
        
        
        
        
        
        