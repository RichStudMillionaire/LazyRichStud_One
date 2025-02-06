from yf_api import Filter
from objects import HardDrive
from objects import TickerExtractor
from objects import StockInfoReader

class GrowthOne():
    def __init__(self):
        self.system_name = "Growth System 1"
        self.boot() 
        self.memory={}

    
    def boot(self):
        self.chunk_size = 150
        m=HardDrive().load("system")
        if m == False:
            print("No system memory")
            nasdaq=TickerExtractor("nasdaq.csv", 'nasdaq')
            nyse=TickerExtractor("nyse.csv",'nyse')
            self.nasdaq_tickers = nasdaq.get_nasdaq_tickers()
            self.nyse_tickers = nyse.get_nyse_tickers()
            s = StockInfoReader()
            self.nasdaq_no_div = s.filter_ticker_list_on_dividends(self.nasdaq_tickers,self.chunk_size, False)
            #s.long_pause(600)
            self.nyse_no_div = s.filter_ticker_list_on_dividends(self.nyse_tickers,self.chunk_size,False)
            self.create_system_hard_drive()
        else:
            self.load_hard_drive()
            
                
    def show_me_what_you_got(self):
        pass
        
        
    def create_system_hard_drive(self):
        data = {'nasdaqTickers': self.nasdaq_no_div, 'nyseTickers': self.nyse_no_div}
        HardDrive().save(data,'system')
        
    def load_hard_drive(self):
        print('Loading System Data...')
        self.memory=HardDrive().load('system')
        self.nasdaq_no_div = self.memory['nasdaqTickers']
        self.nyse_no_div = self.memory['nyseTickers']  
        self.all_tickers_no_div = self.nasdaq_no_div+self.nyse_no_div
        self.run_system()
    
    def run_system(self):
        f=Filter(200)
        l=f.fifty_day_ma_list(self.nasdaq_no_div)
        fl=f.check_gap_higher_than(l, 20)
        f.print_rpt(fl)
        
    
            
        
    

            
        
        
        
    
        
        
        
        
        