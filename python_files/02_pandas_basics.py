# %% [markdown]
# # Module 2: Introduction to Pandas
#
# Pandas is the most powerful Python library for data analysis. It provides data structures and operations for manipulating numerical tables and time series.
#
# ## Learning Objectives
# - Understand DataFrames and Series
# - Read data from CSV and Excel files
# - Select and filter data
# - Sort and explore datasets
# - Perform basic data analysis

# %% [markdown]
# ## 1. Importing Pandas
#
# First, we need to import the pandas library. The standard convention is to import it as `pd`.

# %%
import pandas as pd
import numpy as np

print(f"Pandas version: {pd.__version__}")

# %% [markdown]
# ## 2. Creating DataFrames
#
# A DataFrame is like an Excel spreadsheet - it has rows and columns.

# %%
# Creating a DataFrame from a dictionary
data = {
    'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
    'Category': ['Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics'],
    'Price': [999.99, 24.99, 79.99, 349.99, 149.99],
    'Stock': [15, 150, 75, 30, 60],
    'Rating': [4.5, 4.2, 4.7, 4.4, 4.6]
}

df = pd.DataFrame(data)
print(df)

# %%
# Basic DataFrame information
print("Shape (rows, columns):", df.shape)
print("\nColumn names:", df.columns.tolist())
print("\nData types:")
print(df.dtypes)

# %% [markdown]
# ## 3. Reading Data from Files
#
# In real work, you'll usually read data from CSV or Excel files.

# %%
# Read sales data
df_sales = pd.read_csv('../datasets/sales_data.csv')

print("First few rows:")
print(df_sales.head())

# %%
# Display basic information
print("\nDataset Information:")
print(f"Number of rows: {len(df_sales)}")
print(f"Number of columns: {len(df_sales.columns)}")
print(f"\nColumn names: {df_sales.columns.tolist()}")

# %%
# Summary statistics
print("Statistical Summary:")
print(df_sales.describe())

# %% [markdown]
# ## 4. Exploring Data
#
# Pandas provides many methods to explore your data quickly.

# %%
# View first and last rows
print("First 5 rows:")
print(df_sales.head())

print("\nLast 5 rows:")
print(df_sales.tail())

# %%
# Get detailed information about the dataset
print("Detailed Dataset Info:")
df_sales.info()

# %%
# Check for missing values
print("Missing values per column:")
print(df_sales.isnull().sum())

# %% [markdown]
# ## 5. Selecting Columns
#
# Select specific columns like choosing columns in Excel.

# %%
# Select a single column (returns a Series)
product_ids = df_sales['product_id']
print("Product IDs (Series):")
print(product_ids.head())
print(f"\nType: {type(product_ids)}")

# %%
# Select multiple columns (returns a DataFrame)
sales_subset = df_sales[['date', 'product_id', 'total_amount', 'region']]
print("Selected columns:")
print(sales_subset.head(10))

# %%
# Renaming columns for clarity
sales_renamed = df_sales.rename(columns={
    'total_amount': 'Total_Sales',
    'unit_price': 'Price_Per_Unit'
})
print(sales_renamed.columns.tolist())

# %% [markdown]
# ## 6. Filtering Data
#
# Filter rows based on conditions, similar to Excel filters.

# %%
# Filter: Sales above $1000
high_value_sales = df_sales[df_sales['total_amount'] > 1000]
print(f"High value sales (>${1000}): {len(high_value_sales)} transactions")
print(high_value_sales.head())

# %%
# Filter: Sales from specific region
north_sales = df_sales[df_sales['region'] == 'North']
print(f"\nNorth region sales: {len(north_sales)} transactions")
print(north_sales.head())

# %%
# Multiple conditions with & (and)
north_high_value = df_sales[
    (df_sales['region'] == 'North') & 
    (df_sales['total_amount'] > 500)
]
print(f"\nNorth region high-value sales: {len(north_high_value)} transactions")
print(north_high_value.head())

# %%
# Multiple conditions with | (or)
east_or_west = df_sales[
    (df_sales['region'] == 'East') | 
    (df_sales['region'] == 'West')
]
print(f"\nEast or West sales: {len(east_or_west)} transactions")

# %%
# Using .isin() for multiple values
selected_regions = df_sales[df_sales['region'].isin(['North', 'South', 'Central'])]
print(f"\nSelected regions: {len(selected_regions)} transactions")

# %% [markdown]
# ## 7. Sorting Data

# %%
# Sort by total_amount (ascending)
sorted_asc = df_sales.sort_values('total_amount')
print("Lowest sales:")
print(sorted_asc[['date', 'product_id', 'total_amount', 'region']].head())

# %%
# Sort by total_amount (descending)
sorted_desc = df_sales.sort_values('total_amount', ascending=False)
print("\nHighest sales:")
print(sorted_desc[['date', 'product_id', 'total_amount', 'region']].head())

# %%
# Sort by multiple columns
sorted_multi = df_sales.sort_values(['region', 'total_amount'], ascending=[True, False])
print("\nSorted by region (A-Z) then by amount (high to low):")
print(sorted_multi[['region', 'total_amount']].head(15))

# %% [markdown]
# ## 8. Basic Calculations
#
# Perform calculations on columns easily.

# %%
# Calculate total sales
total_revenue = df_sales['total_amount'].sum()
average_sale = df_sales['total_amount'].mean()
median_sale = df_sales['total_amount'].median()
max_sale = df_sales['total_amount'].max()
min_sale = df_sales['total_amount'].min()

print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Average Sale: ${average_sale:,.2f}")
print(f"Median Sale: ${median_sale:,.2f}")
print(f"Largest Sale: ${max_sale:,.2f}")
print(f"Smallest Sale: ${min_sale:,.2f}")

# %%
# Count unique values
unique_products = df_sales['product_id'].nunique()
unique_customers = df_sales['customer_id'].nunique()
unique_regions = df_sales['region'].nunique()

print(f"\nUnique Products: {unique_products}")
print(f"Unique Customers: {unique_customers}")
print(f"Unique Regions: {unique_regions}")

# %%
# Value counts - frequency of each value
print("\nSales by Region:")
print(df_sales['region'].value_counts())

print("\nSales by Payment Method:")
print(df_sales['payment_method'].value_counts())

# %% [markdown]
# ## 9. Adding New Columns
#
# Create new columns based on existing data.

# %%
# Add a discount column (10% discount)
df_sales['discount_10pct'] = df_sales['total_amount'] * 0.10
df_sales['amount_after_discount'] = df_sales['total_amount'] - df_sales['discount_10pct']

print(df_sales[['total_amount', 'discount_10pct', 'amount_after_discount']].head())

# %%
# Categorize sales as High, Medium, or Low
def categorize_sale(amount):
    if amount >= 1000:
        return 'High'
    elif amount >= 500:
        return 'Medium'
    else:
        return 'Low'

df_sales['sale_category'] = df_sales['total_amount'].apply(categorize_sale)
print(df_sales[['total_amount', 'sale_category']].head(20))

# %%
# Count sales by category
print("\nSales by category:")
print(df_sales['sale_category'].value_counts())

# %% [markdown]
# ## 10. Working with Dates
#
# Convert and manipulate date columns.

# %%
# Convert date column to datetime
df_sales['date'] = pd.to_datetime(df_sales['date'])

# Extract date components
df_sales['year'] = df_sales['date'].dt.year
df_sales['month'] = df_sales['date'].dt.month
df_sales['day_of_week'] = df_sales['date'].dt.day_name()

print(df_sales[['date', 'year', 'month', 'day_of_week']].head(10))

# %%
# Sales by month
print("\nSales count by month:")
print(df_sales['month'].value_counts().sort_index())

print("\nSales by day of week:")
print(df_sales['day_of_week'].value_counts())

# %% [markdown]
# ## Practice Exercise
#
# Load customer data and perform analysis.

# %%
# Load customer data
df_customers = pd.read_csv('../datasets/customer_data.csv')

print("Customer Data Preview:")
print(df_customers.head())
print(f"\nTotal customers: {len(df_customers)}")

# %%
# Exercise 1: Find premium customers
premium_customers = df_customers[df_customers['customer_segment'] == 'Premium']
print(f"Premium customers: {len(premium_customers)}")
print(premium_customers[['first_name', 'last_name', 'customer_segment', 'lifetime_value']].head())

# %%
# Exercise 2: Top 10 customers by lifetime value
top_customers = df_customers.sort_values('lifetime_value', ascending=False).head(10)
print("\nTop 10 customers by lifetime value:")
print(top_customers[['first_name', 'last_name', 'lifetime_value', 'total_purchases']])

# %%
# Exercise 3: Customer statistics by segment
print("\nCustomer statistics by segment:")
for segment in df_customers['customer_segment'].unique():
    segment_data = df_customers[df_customers['customer_segment'] == segment]
    avg_value = segment_data['lifetime_value'].mean()
    count = len(segment_data)
    print(f"{segment}: {count} customers, Avg lifetime value: ${avg_value:,.2f}")

# %% [markdown]
# ## Summary
#
# In this module, you learned:
#
# ✓ **Reading Data**: Load CSV and Excel files into DataFrames  
# ✓ **Exploring Data**: Use head(), tail(), info(), describe()  
# ✓ **Selecting Data**: Choose specific columns  
# ✓ **Filtering Data**: Filter rows based on conditions  
# ✓ **Sorting Data**: Sort by one or multiple columns  
# ✓ **Calculations**: Aggregate functions like sum(), mean(), count()  
# ✓ **Creating Columns**: Add new columns based on calculations  
# ✓ **Working with Dates**: Parse and extract date components
#
# ### Pandas vs Excel
#
# | Excel | Pandas |
# |-------|--------|
# | Open file | `pd.read_csv()` or `pd.read_excel()` |
# | Filter | `df[df['column'] > value]` |
# | Sort | `df.sort_values('column')` |
# | SUM() | `df['column'].sum()` |
# | AVERAGE() | `df['column'].mean()` |
# | COUNTIF() | `df['column'].value_counts()` |
# | New column formula | `df['new_col'] = df['col1'] + df['col2']` |
#
# Next up: **Module 3 - Data Visualization** where we'll create charts and graphs!

