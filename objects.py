# LAZY RICH STUD VERSION 1.0
# OBJECTS AND CLASSES
class TickerExtractor:
    def __init__(self, csv_file):
        self.csv = csv_file
        
class Bank:
    def __init__(self):
        self.balance=0
        self.deposit=0
        self.withdrawal=0
        self.value_of_titles=0
        self.owner_contribution=0
        
    def get_balance(self):
        self.balance = self.owner_contribution+self.value_of_titles
        return "{}$".format(self.balance)
    
    def get_owner_contribution(self):
        return '{}$'.format(self.owner_contribution)
    
    def get_value_in_titles(self):
        return "{}$".format(self.value_of_titles)
    
    def update_value_in_titles(self, new_value_in_titles):
        self.value_of_titles = new_value_in_titles
        self.balance = self.owner_contribution+self.value_of_titles
    
    def account_withdrawal(self, amount_withdrawn):
        self.balance-=amount_withdrawn
        self.owner_contribution-=amount_withdrawn
        
    def account_deposit(self, amount_deposited):
        self.balance+=amount_deposited
        self.owner_contribution+=amount_deposited
        
    def get_roi(self):
        if self.balance != 0:
            roi=int((self.get_balance()-self.get_owner_contribution())/self.balance*100)
            return "{}%".format(roi)
        
        else:
            return 'N/A'
        
        