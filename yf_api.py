from objects import TallyCounter
import time
import yfinance as yf 


class InfoExtractor:
    def __init__(self, chunk_size):
        self.tally = TallyCounter()
        self.chunk_size = chunk_size
    
    def extract_single_ticker(self,ticker):
        self.pause_info_extraction(self.chunk_size)
        try:
            dat = yf.Ticker(ticker)
            self.stock_info=dat.info
            return self.stock_info
        except Exception as e: 
            print("Couldn't extract info from {}\n{}".format(ticker,e))
        
    
    def extract_ticker_list(self, ticker_list):
        list = []
        for ticker in ticker_list:
            t=self.extract_single_ticker(ticker)
            list.append(t)
        self.tally.reset()  
        return list

    
    def print_rpt_single_ticker(self,ticker):
        for key, value in ticker.items():
            print("{} : {}".format(key, value))
    
    def print_rpt_ticker_list(self, ticker_list):
        if len(ticker_list)>0:
            print("{} results match your criteria".format(len(ticker_list)))    
            for ticker in ticker_list:
                for key, value in ticker.items():
                    print("{} : {}".format(key, value))
                print()
        else:
            print("No results match your request")
        
    def hard_pause(self, time_in_seconds):
        print("Zzzz Hard Pause")
        time.sleep(time_in_seconds)
        
    def pause_info_extraction(self, chunk_size):
        self.tally.click()
        if self.tally.count == chunk_size:
            print("Zzzzz Sleeping")
            time.sleep(60)
            self.tally.reset()
            
class Filter:
    def __init__(self, chunk_size):
        self.extractor = InfoExtractor(chunk_size)
        
    def fifty_day_ma(self, ticker_list):
        l=self.extractor.extract_ticker_list(ticker_list)
        filtered_list =[]
        try: 
            for ticker in l:
                d = {}
                ma_50 = ticker["fiftyDayAverage"]
                day_high = ticker["dayHigh"]
                if day_high < ma_50:
                    d["symbol"] = ticker["symbol"]
                    d["fiftyDayAverage"] = ma_50
                    d["dayHigh"] = day_high
                    d["gap"] = (ma_50-day_high)/ma_50*100
                    filtered_list.append(d)
            return filtered_list
        except Exception as e:
            print("A problem occured in fifty_day_ma() function. {}".format(e))
    
    def high_price_target(self, ticker_list):
        l=self.extractor.extract_ticker_list(ticker_list)
        filtered_list =[]
        
        for ticker in l:
            try:
                d = {}
                target_high = ticker["targetHigh"]
                day_high = ticker["dayHigh"]
                if day_high < target_high:
                    d["symbol"] = ticker["symbol"]
                    d["targetHigh"] = target_high
                    d["dayHigh"] = day_high
                    d["gap"] = (target_high-day_high)/target_high*100
                    filtered_list.append(d)
            except Exception as e:
                print("problem occured in High_price_target() function. {}".format(e))
        return filtered_list
            
            
    def check_gap_higher_than(self, filtered_list, gap_higher_than):
        l = filtered_list
        for item in l[:]:
            if item["gap"] < gap_higher_than:
                l.remove(item)
        return l
                
    
    def print_rpt(self, ticker_list):
        self.extractor.print_rpt_ticker_list(ticker_list)
        
            