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

def main_menu():
    while True:
        print("""
MAIN MENU
0 Exit
1 CRUD operations
2 Show top ten companies by criteria\n""")

        print("Enter an option:")
        user_input = input()
        if user_input not in ['0', '1', '2']:
            print("Invalid option!")
        else:
            if user_input == '0':
                print('Have a nice day!')
                break
            elif user_input == '1':
                crud_menu()
            else:
                top_ten_menu()


def crud_menu():
    print("""
CRUD MENU
0 Back
1 Create a company
2 Read a company
3 Update a company
4 Delete a company
5 List all companies\n""")

    print("Enter an option:")
    user_input = input()
    if user_input not in ['0', '1', '2', '3', '4', '5']:
        print("Invalid option!")
    else:
        if user_input == '1':  # DONE!
            create_company()
        elif user_input == '2':  # DONE!
            read_company()
        elif user_input == '3':  # DONE!
            update_company()
        elif user_input == '4':  # DONE!
            delete_company()
        elif user_input == '5':  # DONE!
            list_companies()
        else:  # user asked to go back
            pass


def top_ten_menu():
    print("""
TOP TEN MENU
0 Back
1 List by ND/EBITDA
2 List by ROE
3 List by ROA\n""")

    print("Enter an option:")
    user_input = input()
    if user_input not in ['0', '1', '2', '3']:
        print("Invalid option!")
    else:
        if user_input == '1':
            list_by_nd()
        elif user_input == '2':
            list_by_roe()
        elif user_input == '3':
            list_by_roa()
        else:  # user asked to go back
            pass

# CRUD MENU actions
def create_company():
    print('Not implemented!\n')


def read_company():
    print('Not implemented!\n')


def update_company():
    print('Not implemented!\n')


def delete_company():
    print('Not implemented!\n')


def list_companies():
    print('Not implemented!\n')


# TOP TEN MENU actions
def list_by_nd():
    print('Not implemented!\n')


def list_by_roe():
    print('Not implemented!\n')


def list_by_roa():
    print('Not implemented!\n')
