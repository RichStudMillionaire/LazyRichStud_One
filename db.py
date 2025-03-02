import sqlite3

con = sqlite3.connect('LazyRich.db')
cursor = con.cursor()
cursor.execute("DROP TABLE IF EXISTS stock_purchases")
stock_purchases = """CREATE TABLE stock_purchases (
    symbol VARCHAR (10) NOT NULL,
    buy_price REAL (10) NOT NULL,
    qty INT (100) NOT NULL,
    recommended_sell_price REAL (10) NOT NULL);"""
cursor.execute(stock_purchases)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
fetch = cursor.fetchone()
print(fetch)
