# advanced_sales_analysis.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import statsmodels.api as sm

# Connect to SQLite database
engine = create_engine('sqlite:///amazon_sales_data.db')
query = "SELECT * FROM sales"
data = pd.read_sql(query, con=engine)

# Inspect the data
print("Data Preview:")
print(data.head())

# Convert date column to datetime
data['date'] = pd.to_datetime(data['date'])

# Descriptive statistics
print("\nDescriptive Statistics:")
print(data.describe(include='all'))

# Additional statistical measures
print("\nAdditional Statistical Measures:")
print(f"Mean Sales: {data['sales'].mean()}")
print(f"Median Sales: {data['sales'].median()}")
print(f"Mode Sales: {data['sales'].mode()[0]}")
print(f"Variance in Sales: {data['sales'].var()}")
print(f"Standard Deviation of Sales: {data['sales'].std()}")

# Trend analysis
data['month'] = data['date'].dt.to_period('M')
monthly_sales = data.groupby('month').agg({'sales': 'sum'}).reset_index()

# Plot monthly sales trend
plt.figure(figsize=(12, 6))
plt.plot(monthly_sales['month'].astype(str), monthly_sales['sales'], marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

# Regression Analysis for trend
monthly_sales['month_index'] = range(len(monthly_sales))
X = sm.add_constant(monthly_sales['month_index'])
y = monthly_sales['sales']
model = sm.OLS(y, X).fit()
predictions = model.predict(X)

# Plot regression line
plt.figure(figsize=(12, 6))
plt.scatter(monthly_sales['month_index'], monthly_sales['sales'], color='blue', label='Actual Sales')
plt.plot(monthly_sales['month_index'], predictions, color='red', label='Fitted Line')
plt.title('Sales Trend with Regression Line')
plt.xlabel('Month Index')
plt.ylabel('Sales')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Create optimized SQL views
with engine.connect() as connection:
    connection.execute("""
    CREATE VIEW IF NOT EXISTS sales_summary AS
    SELECT
        product,
        region,
        strftime('%Y-%m', date) AS month,
        SUM(sales) AS total_sales
    FROM sales
    GROUP BY product, region, month
    """)
