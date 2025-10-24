# %% [markdown]
# # Comprehensive Practice Exercises - SOLUTIONS
#
# This notebook contains complete solutions to all exercises.
# Try to complete the exercises on your own first before looking at these solutions!

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("✓ Libraries imported successfully!")

# %% [markdown]
# ## Exercise 1: Python Fundamentals (10 points)
#
# ### Task A: Working with Lists

# %%
monthly_revenue = [18000, 22000, 19500, 25000, 21000, 23500, 26000, 24000, 22500, 27000, 29000, 31000]

# Calculate statistics
total_revenue = sum(monthly_revenue)
average_revenue = total_revenue / len(monthly_revenue)
highest_month = max(monthly_revenue)
lowest_month = min(monthly_revenue)
months_over_20k = len([rev for rev in monthly_revenue if rev > 20000])

print(f"Total Revenue: ${total_revenue:,}")
print(f"Average Monthly Revenue: ${average_revenue:,.2f}")
print(f"Highest Month: ${highest_month:,}")
print(f"Lowest Month: ${lowest_month:,}")
print(f"Months exceeding $20,000: {months_over_20k}")

# %% [markdown]
# ### Task B: Dictionary Operations

# %%
product = {
    'name': 'Wireless Mouse',
    'price': 29.99,
    'quantity': 150,
    'category': 'Electronics'
}

# Calculate total value
total_value = product['price'] * product['quantity']
print(f"Product: {product['name']}")
print(f"Price: ${product['price']}")
print(f"Quantity: {product['quantity']}")
print(f"Total Value: ${total_value:,.2f}")

# %% [markdown]
# ## Exercise 2: Loading and Exploring Data (10 points)

# %%
# Load the data
df_sales = pd.read_csv('../datasets/sales_data.csv', parse_dates=['date'])

# 1. How many transactions?
print(f"1. Total transactions: {len(df_sales):,}")

# 2. Date range
print(f"2. Date range: {df_sales['date'].min().date()} to {df_sales['date'].max().date()}")

# 3. Unique customers
print(f"3. Unique customers: {df_sales['customer_id'].nunique():,}")

# 4. Top 3 payment methods
top_payment = df_sales['payment_method'].value_counts().head(3)
print("\n4. Top 3 payment methods:")
for method, count in top_payment.items():
    print(f"   {method}: {count:,} transactions")

# %% [markdown]
# ## Exercise 3: Filtering and Selection (15 points)

# %%
# 1. Transactions over $1,500
high_value = df_sales[df_sales['total_amount'] > 1500]
print(f"1. Transactions over $1,500: {len(high_value):,}")
print(high_value[['transaction_id', 'total_amount', 'region']].head())

# %%
# 2. Transactions from North or South
north_south = df_sales[df_sales['region'].isin(['North', 'South'])]
print(f"\n2. Transactions from North or South: {len(north_south):,}")
print(north_south[['transaction_id', 'region', 'total_amount']].head())

# %%
# 3. Transactions over $1,000 AND from East
east_high = df_sales[(df_sales['total_amount'] > 1000) & (df_sales['region'] == 'East')]
print(f"\n3. East region transactions over $1,000: {len(east_high):,}")
print(east_high[['transaction_id', 'region', 'total_amount']].head())

# %%
# 4. Select specific columns
selected = df_sales[['date', 'region', 'total_amount']]
print("\n4. Selected columns:")
print(selected.head(10))

# %% [markdown]
# ## Exercise 4: Groupby and Aggregation (20 points)

# %%
# 1. Total sales by region
region_totals = df_sales.groupby('region')['total_amount'].sum().sort_values(ascending=False)
print("1. Total sales by region:")
for region, total in region_totals.items():
    print(f"   {region}: ${total:,.2f}")

# %%
# 2. Average transaction by payment method
payment_avg = df_sales.groupby('payment_method')['total_amount'].mean().sort_values(ascending=False)
print("\n2. Average transaction by payment method:")
for method, avg in payment_avg.items():
    print(f"   {method}: ${avg:,.2f}")

# %%
# 3. Transactions per sales rep
rep_counts = df_sales.groupby('sales_rep').size().sort_values(ascending=False)
print("\n3. Transactions per sales representative:")
for rep, count in rep_counts.items():
    print(f"   {rep}: {count:,} transactions")

# %%
# 4. Summary by region
region_summary = df_sales.groupby('region')['total_amount'].agg([
    ('Total_Sales', 'sum'),
    ('Avg_Sale', 'mean'),
    ('Transaction_Count', 'count')
]).round(2).sort_values('Total_Sales', ascending=False)

print("\n4. Regional summary:")
print(region_summary)

# %% [markdown]
# ## Exercise 5: Data Visualization (20 points)

# %%
# 1. Bar chart: Total sales by region
plt.figure(figsize=(10, 6))
region_totals = df_sales.groupby('region')['total_amount'].sum().sort_values(ascending=False)
plt.bar(region_totals.index, region_totals.values, color='steelblue')
plt.title('Total Sales by Region', fontsize=14, fontweight='bold')
plt.xlabel('Region')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# 2. Line chart: Daily sales trend
plt.figure(figsize=(14, 6))
daily_sales = df_sales.groupby('date')['total_amount'].sum().sort_index()
plt.plot(daily_sales.index, daily_sales.values, linewidth=2, color='green')
plt.title('Daily Sales Trend', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Total Sales ($)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %%
# 3. Pie chart: Payment method distribution
plt.figure(figsize=(10, 8))
payment_counts = df_sales['payment_method'].value_counts()
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
plt.pie(payment_counts.values, labels=payment_counts.index, autopct='%1.1f%%',
        startangle=90, colors=colors)
plt.title('Payment Method Distribution', fontsize=14, fontweight='bold')
plt.axis('equal')
plt.tight_layout()
plt.show()

# %%
# 4. Histogram: Transaction amounts
plt.figure(figsize=(10, 6))
plt.hist(df_sales['total_amount'], bins=40, color='coral', edgecolor='black', alpha=0.7)
plt.axvline(df_sales['total_amount'].mean(), color='red', linestyle='--', 
            linewidth=2, label=f'Mean: ${df_sales["total_amount"].mean():.2f}')
plt.title('Distribution of Transaction Amounts', fontsize=14, fontweight='bold')
plt.xlabel('Transaction Amount ($)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Exercise 6: Merging Data (15 points)

# %%
# 1. Load customer data
df_customers = pd.read_csv('../datasets/customer_data.csv', parse_dates=['signup_date'])

# 2. Merge with sales
df_merged = pd.merge(
    df_sales,
    df_customers[['customer_id', 'customer_segment', 'city', 'state']],
    on='customer_id',
    how='left'
)

print("Merged data sample:")
print(df_merged[['transaction_id', 'customer_id', 'customer_segment', 'total_amount']].head(10))

# %%
# 3. Total sales by customer segment
segment_sales = df_merged.groupby('customer_segment')['total_amount'].sum().sort_values(ascending=False)
print("\nTotal sales by customer segment:")
for segment, total in segment_sales.items():
    print(f"  {segment}: ${total:,.2f}")

# %%
# 4. Top 5 customers by total purchase amount
top_customers = df_merged.groupby('customer_id').agg({
    'total_amount': 'sum',
    'transaction_id': 'count'
}).sort_values('total_amount', ascending=False).head(5)
top_customers.columns = ['Total_Purchased', 'Num_Transactions']

print("\nTop 5 customers by total purchase amount:")
print(top_customers)

# %% [markdown]
# ## Exercise 7: Data Cleaning (20 points)

# %%
# Load survey data
df_survey = pd.read_csv('../datasets/survey_results.csv', parse_dates=['submission_date'])

print("BEFORE CLEANING:")
print(f"Total rows: {len(df_survey)}")
print("\nMissing values per column:")
print(df_survey.isnull().sum())

# %%
# Make a copy for cleaning
df_survey_clean = df_survey.copy()

# 2. Fill missing satisfaction_score with median
median_score = df_survey_clean['satisfaction_score'].median()
df_survey_clean['satisfaction_score'] = df_survey_clean['satisfaction_score'].fillna(median_score)

# 3. Fill missing age_group
df_survey_clean['age_group'] = df_survey_clean['age_group'].fillna('Not specified')

# 4. Remove rows where would_recommend is missing
df_survey_clean = df_survey_clean.dropna(subset=['would_recommend'])

print("\nAFTER CLEANING:")
print(f"Total rows: {len(df_survey_clean)}")
print("\nMissing values per column:")
print(df_survey_clean.isnull().sum())

# %%
# 5. Show before and after counts
print("\nCLEANING SUMMARY:")
print(f"Rows before: {len(df_survey):,}")
print(f"Rows after: {len(df_survey_clean):,}")
print(f"Rows removed: {len(df_survey) - len(df_survey_clean):,} ({(1 - len(df_survey_clean)/len(df_survey))*100:.1f}%)")

# %% [markdown]
# ## Exercise 8: Date/Time Analysis (15 points)

# %%
# 1. Extract month and day_of_week
df_sales['month'] = df_sales['date'].dt.month
df_sales['day_of_week'] = df_sales['date'].dt.day_name()

print("Date components added:")
print(df_sales[['date', 'month', 'day_of_week']].head(10))

# %%
# 2. Total sales by month
monthly_sales = df_sales.groupby('month')['total_amount'].sum().sort_index()
print("\nTotal sales by month:")
for month, total in monthly_sales.items():
    print(f"  Month {month}: ${total:,.2f}")

# %%
# 3. Average sales by day of week
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekly_pattern = df_sales.groupby('day_of_week')['total_amount'].mean().reindex(day_order)

print("\nAverage sales by day of week:")
for day, avg in weekly_pattern.items():
    print(f"  {day}: ${avg:,.2f}")

# %%
# 4. Visualize monthly sales
plt.figure(figsize=(12, 6))
monthly_sales.plot(kind='line', marker='o', linewidth=2, markersize=8, color='purple')
plt.title('Monthly Sales Trend', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Total Sales ($)')
plt.xticks(monthly_sales.index)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Exercise 9: Pivot Tables (15 points)

# %%
# 1. Sales by region and payment method
pivot1 = df_sales.pivot_table(
    values='total_amount',
    index='region',
    columns='payment_method',
    aggfunc='sum',
    fill_value=0
).round(2)

print("1. Sales amount by region and payment method:")
print(pivot1)

# %%
# 2. Transaction count by sales rep and region
pivot2 = df_sales.pivot_table(
    values='transaction_id',
    index='sales_rep',
    columns='region',
    aggfunc='count',
    fill_value=0
)

print("\n2. Transaction count by sales rep and region:")
print(pivot2)

# %%
# 3. Average transaction by quarter and region
df_sales['quarter'] = df_sales['date'].dt.quarter

pivot3 = df_sales.pivot_table(
    values='total_amount',
    index='quarter',
    columns='region',
    aggfunc='mean',
    fill_value=0
).round(2)

print("\n3. Average transaction amount by quarter and region:")
print(pivot3)

# %% [markdown]
# ## Exercise 10: Comprehensive Analysis (20 points)

# %%
# Which sales representatives are performing best, and in which regions?

# 1. Total sales per rep
rep_totals = df_sales.groupby('sales_rep')['total_amount'].sum().sort_values(ascending=False)
print("1. Total sales per sales representative:")
for rep, total in rep_totals.items():
    print(f"   {rep}: ${total:,.2f}")

# %%
# 2. Average transaction size per rep
rep_avg = df_sales.groupby('sales_rep')['total_amount'].mean().sort_values(ascending=False)
print("\n2. Average transaction size per sales representative:")
for rep, avg in rep_avg.items():
    print(f"   {rep}: ${avg:,.2f}")

# %%
# 3. Number of transactions per rep
rep_count = df_sales.groupby('sales_rep').size().sort_values(ascending=False)
print("\n3. Number of transactions per sales representative:")
for rep, count in rep_count.items():
    print(f"   {rep}: {count:,} transactions")

# %%
# 4. Breakdown by region
rep_region_breakdown = df_sales.pivot_table(
    values='total_amount',
    index='sales_rep',
    columns='region',
    aggfunc='sum',
    fill_value=0
).round(2)

print("\n4. Sales by rep and region:")
print(rep_region_breakdown)

# %%
# 5. Visualization of top 5 reps
top_5_reps = rep_totals.head(5)

plt.figure(figsize=(12, 6))
plt.barh(range(len(top_5_reps)), top_5_reps.values, color='teal')
plt.yticks(range(len(top_5_reps)), top_5_reps.index)
plt.xlabel('Total Sales ($)')
plt.title('Top 5 Sales Representatives by Total Sales', fontsize=14, fontweight='bold')
plt.grid(axis='x', alpha=0.3)

# Add value labels
for i, value in enumerate(top_5_reps.values):
    plt.text(value, i, f' ${value:,.0f}', va='center')

plt.tight_layout()
plt.show()

# %% [markdown]
# ## Challenge Exercise: Mini Dashboard (Bonus 30 points)

# %%
# Create a professional dashboard
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Plot 1: Key metrics (Text)
ax1 = fig.add_subplot(gs[0, 0])
ax1.axis('off')
metrics_text = f"""
KEY METRICS

Total Revenue:
${df_sales['total_amount'].sum():,.0f}

Avg Transaction:
${df_sales['total_amount'].mean():,.0f}

Total Transactions:
{len(df_sales):,}

Unique Customers:
{df_sales['customer_id'].nunique():,}

Date Range:
{df_sales['date'].min().date()}
to {df_sales['date'].max().date()}
"""
ax1.text(0.1, 0.5, metrics_text, fontsize=11, verticalalignment='center',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax1.set_title('Overview', fontsize=12, fontweight='bold', loc='left')

# Plot 2: Sales by region
ax2 = fig.add_subplot(gs[0, 1:])
region_sales = df_sales.groupby('region')['total_amount'].sum().sort_values(ascending=False)
ax2.bar(region_sales.index, region_sales.values, color='#2E86AB')
ax2.set_title('Sales by Region', fontsize=12, fontweight='bold')
ax2.set_ylabel('Total Sales ($)')
ax2.grid(axis='y', alpha=0.3)
ax2.tick_params(axis='x', rotation=45)

# Plot 3: Sales trend
ax3 = fig.add_subplot(gs[1, :])
daily_sales = df_sales.groupby('date')['total_amount'].sum().sort_index()
ax3.plot(daily_sales.index, daily_sales.values, linewidth=2, color='#2ECC71')
ax3.set_title('Daily Sales Trend', fontsize=12, fontweight='bold')
ax3.set_ylabel('Sales ($)')
ax3.tick_params(axis='x', rotation=45)
ax3.grid(True, alpha=0.3)

# Plot 4: Payment methods
ax4 = fig.add_subplot(gs[2, :2])
payment_counts = df_sales['payment_method'].value_counts()
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
ax4.pie(payment_counts.values, labels=payment_counts.index, autopct='%1.1f%%',
        colors=colors, textprops={'fontsize': 9})
ax4.set_title('Payment Methods', fontsize=12, fontweight='bold')

# Plot 5: Transaction distribution
ax5 = fig.add_subplot(gs[2, 2])
ax5.hist(df_sales['total_amount'], bins=30, color='coral', edgecolor='black', alpha=0.7)
ax5.axvline(df_sales['total_amount'].mean(), color='red', linestyle='--', linewidth=2)
ax5.set_xlabel('Amount ($)')
ax5.set_ylabel('Frequency')
ax5.set_title('Transaction Distribution', fontsize=12, fontweight='bold')
ax5.tick_params(axis='x', rotation=45)

plt.suptitle('SALES DASHBOARD', fontsize=18, fontweight='bold', y=0.98)
plt.savefig('sales_dashboard.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ Dashboard saved as 'sales_dashboard.png'")

# %% [markdown]
# ## Challenge Exercise: Custom Function (Bonus 20 points)

# %%
def generate_sales_summary(df):
    """
    Generate a sales summary report
    
    Parameters:
    - df: DataFrame with sales data (must have 'total_amount' column)
    
    Returns:
    - str: Formatted summary report
    """
    try:
        # Validate input
        if not isinstance(df, pd.DataFrame):
            return "Error: Input must be a pandas DataFrame"
        
        if 'total_amount' not in df.columns:
            return "Error: DataFrame must have 'total_amount' column"
        
        if len(df) == 0:
            return "Error: DataFrame is empty"
        
        # Calculate metrics
        total_sales = df['total_amount'].sum()
        avg_sale = df['total_amount'].mean()
        median_sale = df['total_amount'].median()
        num_transactions = len(df)
        max_sale = df['total_amount'].max()
        min_sale = df['total_amount'].min()
        
        # Build report
        report = "=" * 50 + "\n"
        report += "SALES SUMMARY REPORT\n"
        report += "=" * 50 + "\n\n"
        
        report += "📊 KEY METRICS\n"
        report += "-" * 50 + "\n"
        report += f"Total Sales:          ${total_sales:>15,.2f}\n"
        report += f"Average Transaction:  ${avg_sale:>15,.2f}\n"
        report += f"Median Transaction:   ${median_sale:>15,.2f}\n"
        report += f"Total Transactions:   {num_transactions:>18,}\n"
        report += f"Largest Sale:         ${max_sale:>15,.2f}\n"
        report += f"Smallest Sale:        ${min_sale:>15,.2f}\n"
        
        # Regional breakdown if available
        if 'region' in df.columns:
            report += "\n🌍 REGIONAL BREAKDOWN\n"
            report += "-" * 50 + "\n"
            regional = df.groupby('region')['total_amount'].agg(['sum', 'count'])
            for region, row in regional.iterrows():
                report += f"{region:12s}: ${row['sum']:>12,.2f} ({int(row['count']):>4,} txns)\n"
        
        report += "\n" + "=" * 50 + "\n"
        
        return report
        
    except Exception as e:
        return f"Error generating report: {str(e)}"

# %%
# Test the function
print(generate_sales_summary(df_sales))

# %%
# Test with a subset
north_sales = df_sales[df_sales['region'] == 'North']
print("\nNORTH REGION ONLY:")
print(generate_sales_summary(north_sales))

# %% [markdown]
# ## Congratulations! 🎉
#
# You've completed all the exercises!
#
# ### Your Learning Journey
#
# ✅ Python fundamentals  
# ✅ Data loading and exploration  
# ✅ Filtering and selection  
# ✅ GroupBy operations  
# ✅ Data visualization  
# ✅ Merging datasets  
# ✅ Data cleaning  
# ✅ Date/time operations  
# ✅ Pivot tables  
# ✅ Creating functions
#
# ### Next Steps
#
# 1. **Review**: Go through any exercises you found challenging
# 2. **Practice**: Try analyzing your own datasets
# 3. **Build**: Create an automated report for work
# 4. **Learn More**: Check out `reference/resources.md` for next topics
#
# ### Keep Learning!
#
# - Join the Python community on Reddit (r/learnpython)
# - Follow data science blogs
# - Practice on Kaggle
# - Build real projects
#
# **You're now equipped to do data analysis with Python!** 🐍📊🚀

