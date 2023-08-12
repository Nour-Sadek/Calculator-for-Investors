# Calculator for Investors

### About

The information from two csv files, companies.csv and financial.csv, will be imported to 
two database tables that hold company information as so:

companies database table:
- ticker TEXT PRIMARY KEY
- name TEXT
- sector TEXT

financial database table:
- ticker TEXT PRIMARY KEY
- ebitda REAL
- sales REAL
- net_profit REAL
- market_price REAL
- net_debt REAL
- assets REAL
- equity REAL
- cash_equivalents REAL
- liabilities REAL

The user will have the option to perform CRUD (Create, Read, Update, Delete) 
operations on these two database tables, or list the top companies based on 
certain analysis made on the financial information available for each company.

### Learning Outcomes
You will get familiar with basic SQL commands, learn how to read files and create 
databases, and find out how to read, update, and delete fields in the database.

# General Info

To learn more about this project, please visit 
[HyperSkill Website - Calculator for Investors](https://hyperskill.org/projects/264).

This project's difficulty has been labelled as __Challenging__ where this is how 
HyperSkill describes each of its four available difficulty levels:

- __Easy Projects__ - if you're just starting
- __Medium Projects__ - to build upon the basics
- __Hard Projects__ - to practice all the basic concepts and learn new ones
- __Challenging Projects__ - to perfect your knowledge with challenging tasks

This repository contains:

    data repository - Contains the 2 csv files from which data were imported into database tables

    analysis.py - Contains the implementation of this program's aim using SQLAlchemy library

    analysis_2.py - Contains the implementation of this program's aim using sqlite3 library

Project was built using python version 3.11.3

# How to Run

Download the project's files (data repository, analysis_2.py and analysis.py) 
to your local repository and open the project in your choice IDE and run either 
analysis_2.py or analysis.py. Both programs will provide the same user interface, but 
will differ in implementation.

After a single run of the program, a database investor.db would have been created in the 
same working directory.
