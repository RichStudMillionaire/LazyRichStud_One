from memory_util import HardDrive
from datetime import datetime
from time_util import Timekeeper
class Report:
    def __init__(self):
        #Started in february 2025
        self.current_month = datetime.today().month
        self.year = 2025
        self.hard_drive = HardDrive()
        self.timekeeper = Timekeeper()
        self.daily_report_dict = {}
        self.daily_report_items=[]
    def add_credit_cards(self, *card_name):
        self.credit_cards = []
        for card in card_name:
            print(card)
            file = card + '.json'
            cc = self.hard_drive.load(file)
            if cc:
                self.credit_cards.append(cc)
    def proceed_to_next_month(self):
        for credit_card in self.credit_cards:
            credit_card['currentMonth'] = self.timekeeper.change_month()
            credit_card['currentYear'] = self.timekeeper.change_year()
    def print_daily_report(self):
        pass
                
    def include_in_daily_report(self, item):
        pass
        
                
                
    
    
        
        
            
            
        
        
        
        
        
        