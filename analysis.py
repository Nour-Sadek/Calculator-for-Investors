# Imported packages
import csv
import sqlite3
from typing import Any

from sqlalchemy import Column, Float, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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
    print('Not implemented!\n')


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
    # Start the program
    main_menu()
