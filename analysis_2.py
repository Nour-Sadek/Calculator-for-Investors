import sqlite3
import csv
from typing import Union

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
    # Read in the required information for the company
    ticker = read_ticker()
    print("Enter company (in the format 'Moon Corp'):")
    company_name = input()
    print("Enter industries (in the format 'Technology'):")
    sector = input()
    ebitda = read_number("ebitda")
    sales = read_number("sales")
    net_profit = read_number("net profit")
    market_price = read_number("market price")
    net_debt = read_number("net debt")
    assets = read_number("assets")
    equity = read_number("equity")
    cash_equivalents = read_number("cash equivalents")
    liabilities = read_number("liabilities")

    # Insert the company into the database
    companies_values = (ticker, company_name, sector)
    financial_values = (ticker, ebitda, sales, net_profit, market_price,
                        net_debt, assets, equity, cash_equivalents, liabilities)
    c.execute("INSERT INTO companies VALUES (?, ?, ?)", companies_values)
    c.execute("INSERT INTO financial VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              financial_values)
    conn.commit()

    print("Company created successfully!")


# create_company helper functions (2)
def read_ticker() -> str:
    while True:
        print("Enter ticker (in the format 'MOON'):")
        ticker = input()
        if ticker.isalpha() and ticker.isupper():
            break
        else:
            print('Wrong format! Please provide ticker in the right format.')
    return ticker


def read_number(identity: str) -> float:
    while True:
        statement = f"Enter {identity} (in the format '987654321'):"
        print(statement)
        value = input()
        try:
            value = float(value)
            return value
        except ValueError:
            print("Wrong input! Please provide a valid number.")


def read_company():
    rows = acquire_companies()
    if rows:
        while True:
            print("Enter company number:")
            user_input = input()
            if user_input not in [str(num) for num in range(len(rows))]:
                print(
                    'Wrong input! Please input an available company number.')
            else:
                ticker = rows[int(user_input)][0]
                name = rows[int(user_input)][1]
                print(f"{ticker} {name}")
                company_info(ticker)
                break


# Helper function for read_company()
def acquire_companies() -> list:
    print("Enter company name:")
    company_name = input()
    command = f"SELECT ticker, name FROM companies WHERE name LIKE '%{company_name}%'"
    c.execute(command)
    rows = c.fetchall()
    if not rows:
        print("Company not found!")
        return []
    else:
        i = 0
        for company in rows:
            print(f"{i} {company[1]}")
            i = i + 1
        return rows


# Helper function for read_company()
def company_info(ticker: str) -> None:
    statement = f"SELECT * FROM financial WHERE ticker = '{ticker}'"
    c.execute(statement)
    values = c.fetchone()

    # get required values
    ebitda = values[1]
    sales = values[2]
    net_profit = values[3]
    market_price = values[4]
    net_debt = values[5]
    assets = values[6]
    equity = values[7]
    liabilities = values[9]

    # Calculating the required info

    print(f"P/E = {calculate_formula(market_price, net_profit)}")
    print(f"P/S = {calculate_formula(market_price, sales)}")
    print(f"P/B = {calculate_formula(market_price, assets)}")
    print(f"ND/EBITDA = {calculate_formula(net_debt, ebitda)}")
    print(f"ROE = {calculate_formula(net_profit, equity)}")
    print(f"ROA = {calculate_formula(net_profit, assets)}")
    print(f"L/A = {calculate_formula(liabilities, assets)}")


# Helper function for company_info()
def calculate_formula(num1: float, num2: float) -> Union[float, None]:
    try:
        value = round(num1 / num2, 2)
    except TypeError:
        value = None
    return value


def update_company():
    rows = acquire_companies()
    if rows:
        while True:
            print("Enter company number:")
            user_input = input()
            if user_input not in [str(num) for num in range(len(rows))]:
                print(
                    'Wrong input! Please input an available company number.')
            else:
                ticker = rows[int(user_input)][0]
                get_and_set_values(ticker)
                print("Company updated successfully!")
                break


# Helper function for update_company()
def get_and_set_values(ticker: str) -> None:
    # Get values from the user
    ebitda = read_number("ebitda")
    sales = read_number("sales")
    net_profit = read_number("net profit")
    market_price = read_number("market price")
    net_debt = read_number("net debt")
    assets = read_number("assets")
    equity = read_number("equity")
    cash_equivalents = read_number("cash equivalents")
    liabilities = read_number("liabilities")

    # Update the database with the new values
    command = f"UPDATE financial SET ebitda = {ebitda}, sales = {sales}, \
    net_profit = {net_profit}, market_price = {market_price}, \
    net_debt = {net_debt}, assets = {assets}, equity = {equity}, \
    cash_equivalents = {cash_equivalents}, liabilities = {liabilities} WHERE ticker = '{ticker}'"
    c.execute(command)
    conn.commit()


def delete_company():
    rows = acquire_companies()
    if rows:
        while True:
            print("Enter company number:")
            user_input = input()
            if user_input not in [str(num) for num in range(len(rows))]:
                print(
                    'Wrong input! Please input an available company number.')
            else:
                ticker = rows[int(user_input)][0]
                command = f"DELETE FROM companies WHERE ticker = '{ticker}'"
                c.execute(command)
                command = f"DELETE FROM financial WHERE ticker = '{ticker}'"
                c.execute(command)
                conn.commit()
                print("Company deleted successfully!")
                break


def list_companies():
    print("COMPANY LIST")
    c.execute("SELECT * FROM companies ORDER BY ticker ASC")
    all_companies = c.fetchall()
    for company in all_companies:
        ticker = company[0]
        name = company[1]
        sector = company[2]
        print(ticker, name, sector)
    print()


def list_top_ten(type_to_list: str, table: str) -> None:
    pass


def create_table(type_to_list: str, table: str) -> None:
    # Create a temporary table to store <type_to_list> values
    command = f"""CREATE TEMPORARY TABLE IF NOT EXISTS {table} (
        ticker TEXT NOT NULL PRIMARY KEY,
        {type_to_list} REAL)"""
    c.execute(command)
    conn.commit()


# TOP TEN MENU actions
def list_by_nd() -> None:
    type_to_list = 'nd_ebitda'
    table = 'companies_' + type_to_list

    # IF NOT EXISTS, create the table and populate it
    create_table(type_to_list, table)

    # Fill out the table if it is empty
    command = f"SELECT * FROM {table}"
    c.execute(command)
    if c.fetchone() is None:
        c.execute('SELECT ticker, net_debt, ebitda FROM financial')
        all_companies = c.fetchall()
        for company in all_companies:
            nd_ebitda = calculate_formula(company[1], company[2])
            c.execute("INSERT INTO companies_nd_ebitda VALUES (?, ?)",
                      (company[0], nd_ebitda))
        conn.commit()

    # Print out the top ten
    list_top_ten(type_to_list, table)


def list_by_roe():
    print('Not implemented!\n')


def list_by_roa():
    print('Not implemented!\n')


if __name__ == '__main__':
    print("Welcome to the Investor Program!")
    main_menu()