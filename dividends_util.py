import sqlite3
from systems_util import DividendSystem

class Dividends:
    def __init__(self):
        self.con = sqlite3.connect('lazyRich.db')
        self.cur = self.con.cursor()
    def add_dividend_stock_to_portfolio(self, symbol, average, qty, system_id):
        dividend_stock = (symbol, average, qty, system_id)
        sql = """INSERT INTO dividends(symbol, average, qty, system_id) VALUES(?,?,?,?) """
        self.cur.execute(sql, dividend_stock)
        self.commit_and_close()
    def empty_table(self):
        self.cur.execute('DELETE FROM dividends')
    def commit_and_close(self):
        self.con.commit()
        self.con.close()
    
system = DividendSystem()
id = system.id
div  = Dividends()
div.add_dividend_stock_to_portfolio('CHRD', 104.06, 1, id)
#div.empty_table()

        
        
    
        