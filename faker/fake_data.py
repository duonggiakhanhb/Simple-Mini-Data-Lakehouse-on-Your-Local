import sqlite3
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import concurrent.futures
import random
from create_table import create_tables

fake = Faker()

numAccounts = 1000 * 100
batch_size = 50000  # Adjust this based on your system's memory capacity

# Connect to the SQLite database (or create a new one if it doesn't exist)
conn = sqlite3.connect('db/bank_data.db')
cursor = conn.cursor()
create_tables(cursor, conn)

# Function to generate fake customer data
def generate_fake_customer(id):
    return {
        'CustomerID': id,
        'FirstName': fake.first_name(),
        'LastName': fake.last_name(),
        'DateOfBirth': fake.date_of_birth().strftime("%Y/%m/%d %H:%M:%S"),
        'ContactPhone': fake.phone_number(),
        'Email': fake.email(),
        'Address': fake.address()
    }

# Function to generate fake account data
def generate_fake_account(args):
    customer_id, account_id = args
    return {
        'AccountID': account_id,
        'CustomerID': customer_id,
        'AccountType': random.choice(['Savings', 'Checking']),
        'Balance': round(random.uniform(1000, 100000), 2),
        'AccountOpenDate': fake.date_between(start_date=datetime.now() - timedelta(days=365), end_date='now').strftime("%Y/%m/%d %H:%M:%S")
    }

# Function to generate fake transaction data
def generate_fake_transaction(args):
    account_id, transaction_id = args
    transaction_date = fake.date_time_between(start_date=datetime.now() - timedelta(days=365), end_date='now')
    transaction_type = random.choice(['Deposit', 'Withdrawal', 'Transfer', 'Payment'])

    if transaction_type in ['Withdrawal', 'Transfer']:
        amount = round(random.uniform(10, 1000), 2) * -1
    else:
        amount = round(random.uniform(10, 1000), 2)

    description = f'{transaction_type} - {fake.word()}'

    return {
        'TransactionID': transaction_id,
        'AccountID': account_id,
        'TransactionDate': transaction_date.strftime("%Y/%m/%d %H:%M:%S"),
        'TransactionType': transaction_type,
        'Amount': amount,
        'Description': description
    }

# Function to generate fake credit card data
def generate_fake_credit_card(args):
    customer_id, credit_card_id = args
    return {
        'CreditCardID': credit_card_id,
        'CardNumber': fake.credit_card_number(card_type='mastercard'),
        'CustomerID': customer_id,
        'CreditLimit': round(random.uniform(1000, 50000), 2),
        'OutstandingBalance': round(random.uniform(0, 5000), 2),
        'CardExpiryDate': fake.date_between(start_date='now', end_date=datetime.now() + timedelta(days=365 * 5)).strftime("%Y/%m/%d %H:%M:%S")
    }

# Function to generate fake investment data
def generate_fake_investment(args):
    customer_id, investment_id = args
    return {
        'InvestmentID': investment_id,
        'CustomerID': customer_id,
        'InvestmentType': random.choice(['Stocks', 'Bonds', 'Mutual Funds']),
        'InvestmentAmount': round(random.uniform(1000, 50000), 2),
        'PurchaseDate': fake.date_between(start_date=datetime.now() - timedelta(days=365), end_date='now').strftime("%Y/%m/%d %H:%M:%S"),
        'CurrentValue': round(random.uniform(800, 120000), 2)
    }

# Function to insert data into SQLite database
def insert_data(table_name, df):
    df.to_sql(table_name, conn, if_exists='replace', index=False)

# Use the auto-incremented ID to generate other data
with concurrent.futures.ThreadPoolExecutor() as executor:
    customers_df = pd.DataFrame(executor.map(generate_fake_customer, range(numAccounts)))
    accounts_df = pd.DataFrame(executor.map(generate_fake_account, zip(customers_df['CustomerID'], range(numAccounts))))
    transactions_df = pd.DataFrame(executor.map(generate_fake_transaction, zip(accounts_df['AccountID'], range(numAccounts))))
    credit_cards_df = pd.DataFrame(executor.map(generate_fake_credit_card, zip(customers_df['CustomerID'], range(numAccounts))))
    investments_df = pd.DataFrame(executor.map(generate_fake_investment, zip(customers_df['CustomerID'], range(numAccounts))))
    print('Generated fake data')

# Insert other data into the SQLite database
insert_data('Customers', customers_df)
insert_data('Accounts', accounts_df)
insert_data('Transactions', transactions_df)
insert_data('CreditCards', credit_cards_df)
insert_data('Investments', investments_df)

# Commit changes to the database
conn.commit()

# Close the database connection
conn.close()
