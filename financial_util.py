from datetime import datetime
from memory_util import HardDrive
from time_util import Timestamp
from time_util import Timekeeper
import requests

class Salary:
    def __init__(self):
        self.xchange = Xchange()
        self.regular_salary = 0
        self.investment_rate = 0.05
        self.lazy_salary = 0
        self.data={}
        self.pay_frequency = 'Biweekly'
        self.raise_frequency = 'Monthly'
        self.raise_rate = .25
    def set_lazy_salary(self, new_salary):
        lazy = {}
        self.lazy_salary = new_salary
        lazy['cad']=self.lazy_salary
        new_usd = self.xchange.in_cad_out_usd(new_salary)
        lazy['usd'] = new_usd
        lazy['cadStr'] = self.xchange.string_cad(new_salary)
        lazy['usdStr'] = self.xchange.string_usd(new_usd)
        self.data['lazySalary'] = lazy
    
    def get_lazy_salary(self):
        return self.lazy_salary
    
    def get_investment_rate(self):
        return '{}%'.format(self.investment_rate*100)
    
    def get_monthly_investment(self):
        investment = self.regular_salary*self.investment_rate
        self.xchange.string_cad(investment)
    
    def get_all_salary_data(self):
        return self.data
    def set_first_day_of_work(self):
        pass
    def print_compensation_report_current(self):
        pass
    def print_compensation_report_history(self):
        pass
    def set_regular_salary(self, regular_salary):
        self.regular_salary = regular_salary
        regular = {}
        regular['cad']=self.regular_salary
        new_usd = self.xchange.in_cad_out_usd(regular_salary)
        regular['usd'] = new_usd
        regular['cadStr'] = self.xchange.string_cad(regular_salary)
        regular['usdStr'] = self.xchange.string_usd(new_usd)
        self.data['regularSalary'] = regular
    def get_regular_salary(self):
        return self.regular_salary

class Ledger:
    def __init__(self):
        self.hard_drive = HardDrive()
        self.time = Timestamp()
        self.value_of_titles = 0
        self.gross_revenue = 0
        self.net_revenue = 0
        self.salary_paid = 0
        self.cash = 0
        self.titles = 0
        self.owner_contributions_total=0
        self.ledger = {}

    def post_owner_cash_contribution(self, amount_cad):
        owner_contribution = {}
        
        usd = Xchange().in_cad_out_usd(amount_cad) 
        owner_contribution['date'] = Timestamp().today()
        owner_contribution['cad'] = amount_cad
        owner_contribution['usd'] = usd
        owner_contribution['cadStr'] = Xchange().string_cad(amount_cad)
        owner_contribution['usdStr'] = Xchange().string_usd(usd)
        owner_contribution['totalCad'] = self.owner_contributions_total
        index = len(self.ledger)
        print(index)
        self.ledger[index] = owner_contribution
    
        
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
    
    def get_value_of_titles(self):
        return self.value_of_titles

class Xchange:
    def __init__(self):
        self.api_key = '47Z4YH7G52K2NFI8'
        self.usd = 'USD'
        self.cad = 'CAD'  
        self.rates = ()
        self.hard_drive = HardDrive()
        self.timeKeeper = Timekeeper()
        self.delayed = False
        self.save_rates()
    def get_rate_usd_to_cad(self, delayed = False):
        if delayed == False:
            print('usd to cad rate fetched from Vantage API')
            url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={self.usd}&to_currency={self.cad}&apikey={self.api_key}'
            response = requests.get(url)
            data = response.json()
            exchange_rate = data['Realtime Currency Exchange Rate']['5. Exchange Rate']
            return float(exchange_rate)
        elif delayed == True:
            rates = self.load_rates()
            return rates[0]
    def get_rate_cad_to_usd(self, delayed=False):
        if delayed == False:
            print("cad to usd rate fetched from Vantage API")
            url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={self.cad}&to_currency={self.usd}&apikey={self.api_key}'
            response = requests.get(url)
            data = response.json()
            exchange_rate = data['Realtime Currency Exchange Rate']['5. Exchange Rate']
            return float(exchange_rate)
        elif delayed == True:
            rates = self.load_rates()
            return rates[1]
    
    def load_rates(self):
        rates = self.hard_drive.load('exchangeRates.json')
        return rates
    def in_cad_out_usd(self, cad_amount):
        rate = self.get_rate_cad_to_usd()
        result = cad_amount*rate
        return result
    def in_usd_out_cad(self, usd_amount):
        rate = self.get_rate_usd_to_cad()
        result = usd_amount*rate
        return result
    def in_cad_out_usd_string(self, cad_amount):
        cad = float(cad_amount)
        result = self.in_cad_out_usd(cad)
        result = round(result,2)
        return '{:.2f} $ USD'.format(result)
    def in_usd_out_cad_string(self, usd_amount):
        usd = float(usd_amount)
        result = self.in_usd_out_cad(usd)
        return '{:.2f} $ CAD'.format(result) 
    def string_cad(self, cad_amount):
        return '{:.2f} $ CAD'.format(cad_amount)
    def string_usd(self, usd_amount):
        return '{:.2f} $ USD'.format(usd_amount)
    def save_rates(self):
        usdcad = self.get_rate_usd_to_cad()
        cadusd = self.get_rate_cad_to_usd()
        last_rate_fetch = datetime.now()
        last_fetch_str = last_rate_fetch.strftime("%H")
        self.rates = (usdcad, cadusd, last_fetch_str)
        self.hard_drive.save(self.rates, 'exchangeRates.json')
        
class CreditCard:
    def __init__(self, card_id_string , first_balance):
        self.id = card_id_string
        self.year = datetime.today().year
        self.month = datetime.today().month
        self.day = datetime.today().day
        self.first_balance = first_balance
        self.balance = first_balance
    def get_card_id_string(self):
        return self.id
    def get_6_months_installment(self, og_balance):
        return round(og_balance/6,2)
    def get_12_months_installment(self, og_balance):
        return round(og_balance/12,2)
    def get_18_months_installment(self,og_balance):
        return round(og_balance/18,2)
    def get_24_months_installment(self,og_balance):
        return round(og_balance/24,2)
    def make_payment(self,amount):
        self.balance-=amount
    def get_balance(self):
        return self.balance
        
class Escrow:
    def __init__(self, balance):
        self.balance = balance
        self.required_amount_2025 = 800
    def set_balance(self,amount):
        self.balance = amount
    def get_required_amount(self):
        return self.required_amount_2025
    def get_balance_string(self):
        return '{}$ CAD'.format(self.balance)
    def get_required_amount_string(self):
        return '{}$ CAD'.format(self.required_amount_2025)