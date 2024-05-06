import pandas as pd
from sqlalchemy import create_engine
import os

# Define the path to the directory containing the CSV files
csv_dir = 'csvFiles'

# Database configuration - Replace with your actual credentials
username = 'ul8ducc4rsifi6gm'
password = 'd91uDaIZV52T6T5Hw97p'
host = 'bbplxthekouxzht12ytn-mysql.services.clever-cloud.com'
port = '3306'
database = 'bbplxthekouxzht12ytn'

# Create the SQL Engine
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

# Function to read and store CSV files to the database
def store_csv_to_db(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            table_name = filename.replace('.csv', '')
            
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            
            # Store the DataFrame in the SQL database
            df.to_sql(table_name, engine, if_exists='replace', index=False)
            print(f'Stored {filename} in database as table {table_name}')

# Run the function
store_csv_to_db(csv_dir)
