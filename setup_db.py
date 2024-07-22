# setup_db.py

import pandas as pd
from sqlalchemy import create_engine

# Load the dataset
data = pd.read_csv('amazon_sales_data.csv')

# Create SQLite database
engine = create_engine('sqlite:///amazon_sales_data.db')

# Write the data to a SQL table
data.to_sql('sales', con=engine, if_exists='replace', index=False)
