# Imported packages
import csv
import sqlite3
import logging

from sqlalchemy import Column, Float, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# To turn off sqlalchemy logger
logging.disable(logging.INFO)

Base = declarative_base()


class Companies(Base):
    __tablename__ = 'companies'

    ticker = Column(String, primary_key=True)
    name = Column(String(30))
    sector = Column(String)


class Financial(Base):
    __tablename__ = 'financial'

    ticker = Column(String, primary_key=True)
    ebitda = Column(Float)
    sales = Column(Float)
    net_profit = Column(Float)
    market_price = Column(Float)
    net_debt = Column(Float)
    assets = Column(Float)
    equity = Column(Float)
    cash_equivalents = Column(Float)
    liabilities = Column(Float)


# Create the sqlite database
sqlite3.connect('investor.db')

# Connect to SQLAlchemy with SQLite dialect and <investor.db> database
engine = create_engine('sqlite:///investor.db', echo=True)

# Save the created tables companies and financial
Base.metadata.create_all(engine)

# Create a Session class
Session = sessionmaker(bind=engine)
session = Session()

# Creating a query object for each table
query_companies = session.query(Companies)
query_financial = session.query(Financial)


def main_menu():
    while True:
        print("""
MAIN MENU
0 Exit
1 CRUD operations
2 Show top ten companies by criteria\n""")

        user_input = input("Enter an option:")
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

    user_input = input("Enter an option:")
    if user_input not in ['0', '1', '2', '3', '4', '5']:
        print("Invalid option!")
    else:
        if user_input == '1':
            create_company()
        elif user_input == '2':
            read_company()
        elif user_input == '3':
            update_company()
        elif user_input == '4':
            delete_company()
        elif user_input == '5':
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

    user_input = input("Enter an option:")
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
    companies_dict = {}
    financial_dict = {}
    # Read in the required information for the company
    ticker = read_ticker()
    companies_dict['ticker'] = ticker
    financial_dict['ticker'] = ticker
    print("Enter company (in the format 'Moon Corp'):")
    companies_dict['name'] = input()
    print("Enter industries (in the format 'Technology'):")
    companies_dict['sector'] = input()
    financial_dict['ebitda'] = read_number("ebitda")
    financial_dict['sales'] = read_number("sales")
    financial_dict['net_profit'] = read_number("net profit")
    financial_dict['market_price'] = read_number("market price")
    financial_dict['net_debt'] = read_number("net debt")
    financial_dict['assets'] = read_number("assets")
    financial_dict['equity'] = read_number("equity")
    financial_dict['cash_equivalents'] = read_number("cash equivalents")
    financial_dict['liabilities'] = read_number("liabilities")

    # Create Companies and Financial objects
    companies_object = Companies(**companies_dict)
    financial_object = Financial(**financial_dict)

    # Add the objects to the database
    session.add(companies_object)
    session.add(financial_object)
    session.commit()

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
    companies_objects = acquire_companies()
    if companies_objects:
        while True:
            print("Enter company number:")
            user_input = input()
            if user_input not in [str(num) for num in range(companies_objects.count())]:
                print(
                    'Wrong input! Please input an available company number.')
            else:
                ticker = companies_objects[int(user_input)].ticker
                name = companies_objects[int(user_input)].name
                print(f"{ticker} {name}")
                company_info(ticker)
                break


# Helper function for read_company()
def acquire_companies():
    print("Enter company name:")
    company_name = input()
    companies_objects = query_companies.filter(
        Companies.name.like("%{}%".format(company_name)))
    if companies_objects.first() is None:
        print("Company not found!")
        return []
    else:
        i = 0
        for company in companies_objects:
            print(f"{i} {company.name}")
            i = i + 1
        return companies_objects


# Helper function for read_company()
def company_info(ticker: str) -> None:
    financial_query = query_financial.filter(Financial.ticker == ticker)
    values = financial_query[0]  # A Financial object

    # get required values
    ebitda = values.ebitda
    sales = values.sales
    net_profit = values.net_profit
    market_price = values.market_price
    net_debt = values.net_debt
    assets = values.assets
    equity = values.equity
    liabilities = values.liabilities

    # Calculating the required info
    print(f"P/E = {calculate_formula(market_price, net_profit)}")
    print(f"P/S = {calculate_formula(market_price, sales)}")
    print(f"P/B = {calculate_formula(market_price, assets)}")
    print(f"ND/EBITDA = {calculate_formula(net_debt, ebitda)}")
    print(f"ROE = {calculate_formula(net_profit, equity)}")
    print(f"ROA = {calculate_formula(net_profit, assets)}")
    print(f"L/A = {calculate_formula(liabilities, assets)}")


# Helper function for company_info()
def calculate_formula(num1: float, num2: float):
    try:
        value = round(num1 / num2, 2)
    except TypeError:
        value = None
    return value


def update_company():
    companies_objects = acquire_companies()
    if companies_objects:
        while True:
            print("Enter company number:")
            user_input = input()
            if user_input not in [str(num) for num in
                                  range(companies_objects.count())]:
                print(
                    'Wrong input! Please input an available company number.')
            else:
                ticker = companies_objects[int(user_input)].ticker
                get_and_set_values(ticker)
                print("Company updated successfully!")
                break


# Helper function for update_company()
def get_and_set_values(ticker: str) -> None:
    # Get values from the user
    financial_dict = {'ebitda': read_number("ebitda"),
                      'sales': read_number("sales"),
                      'net_profit': read_number("net profit"),
                      'market_price': read_number("market price"),
                      'net_debt': read_number("net debt"),
                      'assets': read_number("assets"),
                      'equity': read_number("equity"),
                      'cash_equivalents': read_number("cash equivalents"),
                      'liabilities': read_number("liabilities")}

    # Update the database with the new values
    company_filter = query_financial.filter(Financial.ticker == ticker)
    company_filter.update(financial_dict)
    session.commit()


def delete_company():
    companies_objects = acquire_companies()
    if companies_objects:
        while True:
            print("Enter company number:")
            user_input = input()
            if user_input not in [str(num) for num in
                                  range(companies_objects.count())]:
                print(
                    'Wrong input! Please input an available company number.')
            else:
                ticker = companies_objects[int(user_input)].ticker
                query_financial.filter(Financial.ticker == ticker).delete()
                query_companies.filter(Companies.ticker == ticker).delete()
                session.commit()
                print("Company deleted successfully!")
                break


def list_companies():
    print("COMPANY LIST")
    all_companies = query_companies.order_by(Companies.ticker).all()
    for company in all_companies:
        ticker = company.ticker
        name = company.name
        sector = company.sector
        print(ticker, name, sector)
    print()


# Helper function for TOP TEN MENU functions
def list_top_ten(companies) -> None:
    companies_dict = {}

    for company in companies:
        ticker = company[0]
        evaluated_metric = calculate_formula(company[1], company[2])
        # Don't include the companies that give a None value
        if evaluated_metric is not None:
            companies_dict[ticker] = evaluated_metric

    top_ten = sorted(companies_dict.items(), key=lambda x: x[1], reverse=True)[:10]

    for company in top_ten:
        print(company[0], company[1])


# TOP TEN MENU actions
def list_by_nd():
    all_companies = session.query(Financial.ticker, Financial.net_debt,
                                  Financial.ebitda)

    # Display the top ten
    print("TICKER ND/EBITDA")
    list_top_ten(all_companies)


def list_by_roe():
    all_companies = session.query(Financial.ticker, Financial.net_profit,
                                  Financial.equity)

    # Display the top ten
    print("TICKER ROE")
    list_top_ten(all_companies)


def list_by_roa():
    all_companies = session.query(Financial.ticker, Financial.net_profit,
                                  Financial.assets)

    # Display the top ten
    print("TICKER ROA")
    list_top_ten(all_companies)


# Read the data from the financial.csv file
with open('data/financial.csv', 'r') as financials:
    financials_reader = csv.DictReader(financials, delimiter=',')
    financial_objects = []
    for row in financials_reader:
        for key in row:
            if row[key] == '':
                row[key] = None
        financial_objects.append(Financial(**row))

    # Insert data from <financial_reader> to financial table in <investor.db>
    # Create a session to modify database
    Session = sessionmaker(bind=engine)
    session = Session()
    # Add the data
    if session.query(Financial).first() is None:  # Checks if table is empty
        for row in financial_objects:
            session.add(row)
    session.commit()
    session.close()

# Read the data from the companies.csv file
with open('data/companies.csv', 'r') as companies:
    companies_reader = csv.DictReader(companies, delimiter=',')
    companies_objects = []
    for row in companies_reader:
        for key in row:
            if row[key] == '':
                row[key] = None
        companies_objects.append(Companies(**row))

    # Insert data from <companies_reader> to companies table in <investor.db>
    # Create a session to modify database
    Session = sessionmaker(bind=engine)
    session = Session()
    # Add the data
    if session.query(Companies).first() is None:  # Checks if table is empty
        for row in companies_objects:
            session.add(row)
    session.commit()
    session.close()

if __name__ == '__main__':
    print("Welcome to the Investor Program!")
    # Start the program
    main_menu()
