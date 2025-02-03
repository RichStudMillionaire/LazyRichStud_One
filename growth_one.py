from objects import LogManager
from objects import TimeManager
from objects import TickerExtractor
from objects import StockInfoReader
from objects import HardDrive

class GrowthOne():
    def __init__(self):
        self.system_name = "Growth System 1"
        self.boot() 
    
    def boot(self):
        m=HardDrive().load("system")
        if m == False:
            print("No system memory")
            nasdaq=TickerExtractor("nasdaq.csv", 'nasdaq')
            nyse=TickerExtractor("nyse.csv",'nyse')
            self.nasdaq_tickers = nasdaq.get_nasdaq_tickers()
            self.nyse_tickers = nyse.get_nyse_tickers()
            s = StockInfoReader()
            self.nasdaq_no_div = s.filter_ticker_list_on_dividends(self.nasdaq_tickers,100, False)
            s.long_pause(600)
            self.nyse_no_div = s.filter_ticker_list_on_dividends(self.nyse_tickers,100,False)
            self.create_system_hard_drive()
        else:
            print("Load System Data")
                
    def show_me_what_you_got(self):
        pass
        
    def create_system_hard_drive(self):
        data = {'nasdaqTickers': self.nasdaq_no_div, 'nyseTickers': self.nyse_no_div}
        HardDrive().save(data,'system')
        
    
        
        
        
        
        