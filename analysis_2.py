import sqlite3
import csv

conn = sqlite3.connect('investor.db')

c = conn.cursor()

# Create the companies table
c.execute("""CREATE TABLE IF NOT EXISTS companies (
ticker TEXT NOT NULL PRIMARY KEY,
name TEXT,
sector TEXT)""")

# Create the financial table
c.execute("""CREATE TABLE IF NOT EXISTS financial (
ticker TEXT NOT NULL PRIMARY KEY,
ebitda REAL,
sales REAL,
net_profit REAL,
market_price REAL,
net_debt REAL,
assets REAL,
equity REAL,
cash_equivalents REAL,
liabilities REAL)""")

conn.commit()


# Insert the data from data/companies.csv to companies table
c.execute('SELECT * FROM companies')
if c.fetchone() is None:
    with open("data/companies.csv", 'r') as companies:
        companies_reader = csv.DictReader(companies, delimiter=',')
        for row in companies_reader:
            values_of_row = []
            for key in row:
                if row[key] == '':
                    row[key] = (None,)
                values_of_row.append(row[key])
            values_of_row = tuple(values_of_row)
            c.execute('INSERT INTO companies VALUES (?, ?, ?)', values_of_row)
            conn.commit()

# Insert the data from data/financial.csv to financial table
c.execute('SELECT * FROM financial')
if c.fetchone() is None:
    with open("data/financial.csv", 'r') as financials:
        financials_reader = csv.DictReader(financials, delimiter=',')
        for row in financials_reader:
            values_of_row = []
            for key in row:
                if row[key] == '':
                    row[key] = None
                values_of_row.append(row[key])
            values_of_row = tuple(values_of_row)
            c.execute(
                'INSERT INTO financial VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                values_of_row)
            conn.commit()
