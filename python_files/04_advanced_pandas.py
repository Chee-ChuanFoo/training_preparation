# %% [markdown]
# # Module 4: Advanced Pandas Operations
#
# Master powerful data analysis techniques that go beyond basic filtering and selection.
#
# ## Learning Objectives
# - Use GroupBy for aggregations
# - Merge and join multiple datasets
# - Create pivot tables
# - Reshape data with melt, stack, and unstack
# - Understand different types of joins

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("Libraries loaded!")

# %%
# Load datasets
df_sales = pd.read_csv('../datasets/sales_data.csv', parse_dates=['date'])
df_customers = pd.read_csv('../datasets/customer_data.csv', parse_dates=['signup_date'])
df_products = pd.read_csv('../datasets/product_catalog.csv')

print("Datasets loaded successfully!")
print(f"Sales records: {len(df_sales)}")
print(f"Customers: {len(df_customers)}")
print(f"Products: {len(df_products)}")

# %% [markdown]
# ## 1. GroupBy - The Split-Apply-Combine Pattern
#
# GroupBy is one of the most powerful operations in Pandas. It's like Pivot Tables in Excel.

# %%
# Simple groupby: Total sales by region
region_totals = df_sales.groupby('region')['total_amount'].sum()
print("Total sales by region:")
print(region_totals)
print(f"\nType: {type(region_totals)}")

# %%
# Multiple aggregations at once
region_stats = df_sales.groupby('region')['total_amount'].agg(['sum', 'mean', 'count', 'min', 'max'])
print("Regional sales statistics:")
print(region_stats)

# %%
# Custom column names for aggregations
region_analysis = df_sales.groupby('region')['total_amount'].agg([
    ('Total_Sales', 'sum'),
    ('Average_Sale', 'mean'),
    ('Number_of_Transactions', 'count'),
    ('Min_Sale', 'min'),
    ('Max_Sale', 'max')
]).round(2)

print(region_analysis)

# %%
# Multiple columns in groupby
rep_region_sales = df_sales.groupby(['region', 'sales_rep'])['total_amount'].sum().reset_index()
print("Sales by region and sales rep:")
print(rep_region_sales.head(20))

# %%
# Visualize groupby results
region_rep_pivot = df_sales.groupby(['region', 'sales_rep'])['total_amount'].sum().unstack(fill_value=0)

plt.figure(figsize=(12, 6))
region_rep_pivot.plot(kind='bar', stacked=False)
plt.title('Sales by Region and Sales Representative', fontsize=14, fontweight='bold')
plt.xlabel('Region')
plt.ylabel('Total Sales ($)')
plt.legend(title='Sales Rep', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 2. Advanced GroupBy Operations

# %%
# Group by multiple columns with multiple aggregations
sales_analysis = df_sales.groupby(['region', 'payment_method']).agg({
    'total_amount': ['sum', 'mean', 'count'],
    'quantity': ['sum', 'mean']
}).round(2)

print("Detailed sales analysis:")
print(sales_analysis.head(15))

# %%
# Using .transform() - keeps original DataFrame shape
df_sales['region_total'] = df_sales.groupby('region')['total_amount'].transform('sum')
df_sales['region_avg'] = df_sales.groupby('region')['total_amount'].transform('mean')
df_sales['pct_of_region_total'] = (df_sales['total_amount'] / df_sales['region_total'] * 100).round(2)

print("Sales with region context:")
print(df_sales[['region', 'total_amount', 'region_total', 'region_avg', 'pct_of_region_total']].head(15))

# %%
# Filtering groups
large_regions = df_sales.groupby('region').filter(lambda x: x['total_amount'].sum() > 100000)
print(f"\nRegions with total sales > $100,000: {large_regions['region'].nunique()} regions")
print(f"Transactions from these regions: {len(large_regions)}")

# %% [markdown]
# ## 3. Time-Based GroupBy

# %%
# Sales by month
df_sales['year_month'] = df_sales['date'].dt.to_period('M')
monthly_sales = df_sales.groupby('year_month')['total_amount'].sum()

print("Monthly sales:")
print(monthly_sales)

# %%
# Visualize monthly trend
plt.figure(figsize=(12, 6))
monthly_sales.plot(kind='line', marker='o', linewidth=2, markersize=8)
plt.title('Monthly Sales Trend', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# Sales by day of week
df_sales['day_of_week'] = df_sales['date'].dt.day_name()
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
daily_pattern = df_sales.groupby('day_of_week')['total_amount'].agg(['sum', 'mean', 'count'])
daily_pattern = daily_pattern.reindex(day_order)

print("Sales pattern by day of week:")
print(daily_pattern)

# %%
# Visualize weekly pattern
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

ax1.bar(daily_pattern.index, daily_pattern['sum'], color='steelblue')
ax1.set_title('Total Sales by Day of Week')
ax1.set_ylabel('Total Sales ($)')
ax1.tick_params(axis='x', rotation=45)

ax2.bar(daily_pattern.index, daily_pattern['mean'], color='coral')
ax2.set_title('Average Transaction by Day of Week')
ax2.set_ylabel('Average Sale ($)')
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# %% [markdown]
# ## 4. Merging DataFrames
#
# Combine multiple datasets, like VLOOKUP in Excel but much more powerful!

# %%
# Preview our datasets
print("Sales data sample:")
print(df_sales[['transaction_id', 'customer_id', 'product_id', 'total_amount']].head())

print("\nCustomer data sample:")
print(df_customers[['customer_id', 'first_name', 'last_name', 'customer_segment']].head())

print("\nProduct data sample:")
print(df_products[['product_id', 'product_name', 'category', 'retail_price']].head())

# %%
# Inner join: Merge sales with customer data
sales_with_customers = pd.merge(
    df_sales,
    df_customers[['customer_id', 'first_name', 'last_name', 'customer_segment', 'city']],
    on='customer_id',
    how='inner'
)

print("Sales with customer information:")
print(sales_with_customers[['transaction_id', 'first_name', 'last_name', 
                             'customer_segment', 'total_amount']].head(10))

# %%
# Merge with products too
sales_complete = pd.merge(
    sales_with_customers,
    df_products[['product_id', 'product_name', 'category']],
    on='product_id',
    how='left'
)

print("\nComplete sales information:")
print(sales_complete[['transaction_id', 'first_name', 'last_name', 'product_name', 
                       'category', 'total_amount']].head(10))

# %% [markdown]
# ### Types of Joins
#
# - **Inner**: Only matching records from both tables
# - **Left**: All records from left table, matching from right
# - **Right**: All records from right table, matching from left
# - **Outer**: All records from both tables

# %%
# Analysis with merged data: Sales by customer segment
segment_analysis = sales_with_customers.groupby('customer_segment').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique'
}).round(2)
segment_analysis.columns = ['Total_Sales', 'Avg_Transaction', 'Num_Transactions', 'Num_Customers']

print("Analysis by customer segment:")
print(segment_analysis)

# %%
# Visualize segment analysis
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

segment_analysis['Total_Sales'].plot(kind='bar', ax=ax1, color='teal')
ax1.set_title('Total Sales by Customer Segment')
ax1.set_ylabel('Total Sales ($)')
ax1.set_xlabel('Segment')
ax1.tick_params(axis='x', rotation=45)

segment_analysis['Avg_Transaction'].plot(kind='bar', ax=ax2, color='coral')
ax2.set_title('Average Transaction by Customer Segment')
ax2.set_ylabel('Average Transaction ($)')
ax2.set_xlabel('Segment')
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()

# %%
# Category analysis with complete data
category_analysis = sales_complete.groupby('category').agg({
    'total_amount': 'sum',
    'transaction_id': 'count',
    'customer_id': 'nunique'
}).round(2)
category_analysis.columns = ['Total_Sales', 'Num_Transactions', 'Unique_Customers']
category_analysis = category_analysis.sort_values('Total_Sales', ascending=False)

print("\nSales by product category:")
print(category_analysis)

# %% [markdown]
# ## 5. Pivot Tables
#
# Reshape data for analysis - exactly like Excel Pivot Tables!

# %%
# Simple pivot table: Sales by region and payment method
pivot_simple = df_sales.pivot_table(
    values='total_amount',
    index='region',
    columns='payment_method',
    aggfunc='sum',
    fill_value=0
).round(2)

print("Sales by region and payment method:")
print(pivot_simple)

# %%
# Visualize pivot table as heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(pivot_simple, annot=True, fmt='.0f', cmap='YlOrRd', cbar_kws={'label': 'Sales ($)'})
plt.title('Sales Heatmap: Region vs Payment Method', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# %%
# Pivot with multiple aggregations
pivot_multi = df_sales.pivot_table(
    values='total_amount',
    index='region',
    columns='payment_method',
    aggfunc=['sum', 'mean', 'count'],
    fill_value=0
).round(2)

print("\nPivot with multiple aggregations:")
print(pivot_multi)

# %%
# Time-based pivot table
df_sales['month'] = df_sales['date'].dt.month
pivot_time = df_sales.pivot_table(
    values='total_amount',
    index='month',
    columns='region',
    aggfunc='sum',
    fill_value=0
).round(2)

print("\nMonthly sales by region:")
print(pivot_time)

# %%
# Visualize time pivot
plt.figure(figsize=(14, 6))
pivot_time.plot(kind='line', marker='o', linewidth=2)
plt.title('Monthly Sales Trend by Region', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 6. Cross-Tabulation
#
# Count frequency of combinations.

# %%
# Cross-tab: Count of transactions by region and payment method
crosstab = pd.crosstab(
    df_sales['region'],
    df_sales['payment_method'],
    margins=True,  # Add row and column totals
    margins_name='Total'
)

print("Transaction counts:")
print(crosstab)

# %%
# Cross-tab with percentages
crosstab_pct = pd.crosstab(
    df_sales['region'],
    df_sales['payment_method'],
    normalize='all'  # 'all', 'index', or 'columns'
) * 100

print("\nTransaction distribution (%):")
print(crosstab_pct.round(2))

# %%
# Visualize cross-tab
plt.figure(figsize=(12, 6))
sns.heatmap(crosstab.iloc[:-1, :-1], annot=True, fmt='d', cmap='Blues', 
            cbar_kws={'label': 'Count'})
plt.title('Transaction Count: Region vs Payment Method', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 7. Reshaping Data

# %%
# Create sample wide data
wide_data = df_sales.groupby(['region', 'month'])['total_amount'].sum().unstack(fill_value=0)
print("Wide format:")
print(wide_data)

# %%
# Melt: Wide to long format
long_data = wide_data.reset_index().melt(
    id_vars='region',
    var_name='month',
    value_name='sales'
)
print("\nLong format:")
print(long_data.head(15))

# %%
# Stack and unstack
# Stack: Move column index to row index
stacked = pivot_simple.stack()
print("Stacked:")
print(stacked.head(10))

# %%
# Unstack: Move row index to column index
unstacked = stacked.unstack()
print("\nUnstacked (back to pivot):")
print(unstacked)

# %% [markdown]
# ## Practice Exercise
#
# Comprehensive analysis combining all techniques!

# %%
# Exercise: Top performing sales reps analysis

# Step 1: Merge sales with customer and product data
complete_data = pd.merge(
    df_sales,
    df_customers[['customer_id', 'customer_segment']],
    on='customer_id',
    how='left'
)

complete_data = pd.merge(
    complete_data,
    df_products[['product_id', 'category']],
    on='product_id',
    how='left'
)

# Step 2: Analyze by sales rep
rep_performance = complete_data.groupby('sales_rep').agg({
    'total_amount': ['sum', 'mean', 'count'],
    'customer_id': 'nunique',
    'transaction_id': 'count'
}).round(2)
rep_performance.columns = ['Total_Sales', 'Avg_Transaction', 'Num_Transactions', 
                            'Unique_Customers', 'Total_Transactions']
rep_performance = rep_performance.sort_values('Total_Sales', ascending=False)

print("Sales representative performance:")
print(rep_performance)

# %%
# Step 3: Category breakdown per rep
rep_category = complete_data.pivot_table(
    values='total_amount',
    index='sales_rep',
    columns='category',
    aggfunc='sum',
    fill_value=0
).round(2)

print("\nSales by rep and category:")
print(rep_category)

# %%
# Step 4: Visualize top performers
top_reps = rep_performance.head(5)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

top_reps['Total_Sales'].plot(kind='barh', ax=ax1, color='steelblue')
ax1.set_title('Top 5 Sales Reps by Total Sales', fontweight='bold')
ax1.set_xlabel('Total Sales ($)')

top_reps['Avg_Transaction'].plot(kind='barh', ax=ax2, color='coral')
ax2.set_title('Top 5 Sales Reps by Avg Transaction', fontweight='bold')
ax2.set_xlabel('Average Transaction ($)')

plt.tight_layout()
plt.show()

# %% [markdown]
# ## Summary
#
# In this module, you learned:
#
# ✓ **GroupBy**: Split-apply-combine pattern for aggregations  
# ✓ **Multiple Aggregations**: Apply multiple functions at once  
# ✓ **Transform**: Add group statistics to original DataFrame  
# ✓ **Merging**: Combine multiple datasets (like VLOOKUP++)  
# ✓ **Join Types**: Inner, left, right, and outer joins  
# ✓ **Pivot Tables**: Reshape data for analysis  
# ✓ **Cross-Tabulation**: Count combinations of categorical variables  
# ✓ **Reshaping**: Melt, stack, and unstack operations
#
# ### Quick Reference
#
# ```python
# # GroupBy
# df.groupby('column')['value'].sum()
# df.groupby('col').agg(['sum', 'mean', 'count'])
#
# # Merge
# pd.merge(df1, df2, on='key', how='inner')
#
# # Pivot Table
# df.pivot_table(values='val', index='row', columns='col', aggfunc='sum')
#
# # Cross-tab
# pd.crosstab(df['col1'], df['col2'])
# ```
#
# Next up: **Module 5 - Data Cleaning & Transformation**!

