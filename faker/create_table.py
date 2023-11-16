import sqlite3

# Create tables
def create_tables(cursor, conn):
    # Create the Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            CustomerID INTEGER PRIMARY KEY AUTOINCREMENT ,
            FirstName TEXT,
            LastName TEXT,
            DateOfBirth DATE,
            ContactPhone TEXT,
            Email TEXT,
            Address TEXT
        )
    ''')

    # Create the Accounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Accounts (
            AccountID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INTEGER,
            AccountType TEXT,
            Balance REAL,
            AccountOpenDate DATE,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
        )
    ''')

    # Create the Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Transactions (
            TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
            AccountID INTEGER,
            TransactionDate DATE,
            TransactionType TEXT,
            Amount REAL,
            Description TEXT
        )
    ''')

    # Create the Credit Cards table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CreditCards (
            CardNumber INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INTEGER,
            CreditLimit REAL,
            OutstandingBalance REAL,
            CardExpiryDate DATE,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
        )
    ''')

    # Create the Investments table (if applicable)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Investments (
            InvestmentID INTEGER PRIMARY KEY AUTOINCREMENT,
            CustomerID INTEGER,
            InvestmentType TEXT,
            InvestmentAmount REAL,
            PurchaseDate DATE,
            CurrentValue REAL,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
        )
    ''')

    # Commit the changes and close the database connection
    conn.commit()

