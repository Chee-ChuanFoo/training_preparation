# %% [markdown]
# # Module 5: Data Cleaning & Transformation
#
# Real-world data is messy! In this module, we'll learn to clean and prepare data for analysis.
#
# ## Learning Objectives
# - Identify and handle missing data
# - Remove duplicates
# - Convert data types
# - Clean and manipulate text
# - Work with dates and times
# - Handle outliers

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

print("Libraries loaded!")

# %% [markdown]
# ## 1. Loading Messy Data
#
# Let's work with survey data that has missing values and inconsistencies.

# %%
# Load survey data (intentionally messy!)
df_survey = pd.read_csv('../datasets/survey_results.csv', parse_dates=['submission_date'])

print("Survey data loaded!")
print(f"Shape: {df_survey.shape}")
print("\nFirst few rows:")
print(df_survey.head(10))

# %%
# Get overview of the data
print("Data Information:")
df_survey.info()

# %% [markdown]
# ## 2. Identifying Missing Data
#
# First step in data cleaning: find the missing values.

# %%
# Count missing values per column
print("Missing values per column:")
missing_counts = df_survey.isnull().sum()
print(missing_counts)

# %%
# Calculate percentage of missing values
print("\nMissing values percentage:")
missing_pct = (df_survey.isnull().sum() / len(df_survey) * 100).round(2)
missing_pct = missing_pct[missing_pct > 0].sort_values(ascending=False)
print(missing_pct)

# %%
# Visualize missing data
plt.figure(figsize=(10, 6))
missing_pct.plot(kind='barh', color='coral')
plt.title('Percentage of Missing Values by Column', fontsize=14, fontweight='bold')
plt.xlabel('Missing (%)')
plt.tight_layout()
plt.show()

# %%
# Visual heatmap of missing values
plt.figure(figsize=(12, 8))
sns.heatmap(df_survey.isnull(), cbar=True, yticklabels=False, cmap='viridis')
plt.title('Missing Data Pattern', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 3. Handling Missing Data
#
# Different strategies for different situations.

# %%
# Strategy 1: Drop rows with ANY missing values
df_complete = df_survey.dropna()
print(f"Original size: {len(df_survey)} rows")
print(f"After dropping all missing: {len(df_complete)} rows")
print(f"Lost {len(df_survey) - len(df_complete)} rows ({(1 - len(df_complete)/len(df_survey))*100:.1f}%)")

# %%
# Strategy 2: Drop rows with missing values in specific columns
df_key_columns = df_survey.dropna(subset=['satisfaction_score', 'would_recommend'])
print(f"\nAfter dropping rows with missing satisfaction or recommendation: {len(df_key_columns)} rows")

# %%
# Strategy 3: Fill missing values with a specific value
df_filled = df_survey.copy()
df_filled['comments'] = df_filled['comments'].fillna('No comment')
df_filled['age_group'] = df_filled['age_group'].fillna('Not specified')

print("\nAfter filling missing values:")
print(df_filled[['response_id', 'age_group', 'comments']].head(10))

# %%
# Strategy 4: Fill with statistical measures
# For numerical data, use mean, median, or mode
df_numeric = df_survey.copy()

# Fill satisfaction_score with median
median_satisfaction = df_survey['satisfaction_score'].median()
df_numeric['satisfaction_score'] = df_survey['satisfaction_score'].fillna(median_satisfaction)

print(f"Filled satisfaction_score missing values with median: {median_satisfaction}")
print(f"Missing satisfaction scores: {df_numeric['satisfaction_score'].isnull().sum()}")

# %%
# Strategy 5: Forward fill or backward fill (useful for time series)
df_ffill = df_survey.copy()
df_ffill['age_group'] = df_ffill['age_group'].fillna(method='ffill')

print("\nForward fill example:")
print(df_ffill[['response_id', 'age_group']].head(20))

# %% [markdown]
# ## 4. Removing Duplicates

# %%
# Check for duplicates
print(f"Total rows: {len(df_survey)}")
print(f"Duplicate rows: {df_survey.duplicated().sum()}")

# %%
# Let's create some duplicates for demonstration
df_with_dupes = pd.concat([df_survey, df_survey.head(20)])
print(f"\nAfter adding duplicates: {len(df_with_dupes)} rows")
print(f"Duplicates: {df_with_dupes.duplicated().sum()}")

# %%
# Remove duplicates
df_no_dupes = df_with_dupes.drop_duplicates()
print(f"\nAfter removing duplicates: {len(df_no_dupes)} rows")

# %%
# Remove duplicates based on specific columns
df_no_dupes_subset = df_with_dupes.drop_duplicates(subset=['response_id'])
print(f"After removing duplicates by response_id: {len(df_no_dupes_subset)} rows")

# %% [markdown]
# ## 5. Data Type Conversion
#
# Ensure columns have the correct data types.

# %%
# Check current data types
print("Current data types:")
print(df_survey.dtypes)

# %%
# Load sales data for type conversion examples
df_sales = pd.read_csv('../datasets/sales_data.csv')
print("\nSales data types:")
print(df_sales.dtypes)

# %%
# Convert date strings to datetime
df_sales['date'] = pd.to_datetime(df_sales['date'])
print("\nAfter converting date:")
print(df_sales.dtypes)
print(df_sales['date'].head())

# %%
# Convert numeric columns stored as strings
# Create example with price as string
df_example = pd.DataFrame({
    'product': ['A', 'B', 'C'],
    'price': ['10.99', '25.50', '15.75'],
    'quantity': ['100', '200', '150']
})

print("Before conversion:")
print(df_example.dtypes)
print(df_example)

# %%
# Convert to numeric
df_example['price'] = pd.to_numeric(df_example['price'])
df_example['quantity'] = pd.to_numeric(df_example['quantity'])

print("\nAfter conversion:")
print(df_example.dtypes)
print(df_example)

# %%
# Convert to categorical (saves memory for repeated values)
df_sales['region'] = df_sales['region'].astype('category')
df_sales['payment_method'] = df_sales['payment_method'].astype('category')

print("\nAfter categorical conversion:")
print(df_sales.dtypes)
print(f"\nRegion categories: {df_sales['region'].cat.categories.tolist()}")

# %% [markdown]
# ## 6. String Operations
#
# Clean and manipulate text data.

# %%
# Load customer data
df_customers = pd.read_csv('../datasets/customer_data.csv')
print("Customer names:")
print(df_customers[['first_name', 'last_name', 'email']].head(10))

# %%
# Convert to lowercase
df_customers['email_lower'] = df_customers['email'].str.lower()
print("\nLowercase emails:")
print(df_customers[['email', 'email_lower']].head())

# %%
# Convert to uppercase
df_customers['state_upper'] = df_customers['state'].str.upper()
print("\nUppercase states:")
print(df_customers[['state', 'state_upper']].head())

# %%
# Strip whitespace
df_messy = pd.DataFrame({
    'name': ['  John  ', 'Mary   ', '  Bob']
})
df_messy['name_clean'] = df_messy['name'].str.strip()
print("\nBefore and after strip:")
print(df_messy)

# %%
# Replace text
df_customers['email_domain'] = df_customers['email'].str.replace('email.com', 'company.com')
print("\nReplaced email domains:")
print(df_customers[['email', 'email_domain']].head())

# %%
# Extract parts of strings
df_customers['email_username'] = df_customers['email'].str.split('@').str[0]
df_customers['email_domain_only'] = df_customers['email'].str.split('@').str[1]

print("\nSplit email:")
print(df_customers[['email', 'email_username', 'email_domain_only']].head())

# %%
# Check if string contains text
df_customers['is_california'] = df_customers['state'].str.contains('CA')
print("\nCalifornia customers:")
print(df_customers[['first_name', 'last_name', 'state', 'is_california']].head(20))

# %%
# String length
df_customers['name_length'] = df_customers['first_name'].str.len()
print("\nName lengths:")
print(df_customers[['first_name', 'name_length']].head(10))

# %% [markdown]
# ## 7. Working with Dates and Times

# %%
# Extract date components
df_sales['year'] = df_sales['date'].dt.year
df_sales['month'] = df_sales['date'].dt.month
df_sales['day'] = df_sales['date'].dt.day
df_sales['day_of_week'] = df_sales['date'].dt.day_name()
df_sales['quarter'] = df_sales['date'].dt.quarter

print("Date components:")
print(df_sales[['date', 'year', 'month', 'day', 'day_of_week', 'quarter']].head(10))

# %%
# Calculate time differences
df_customers['signup_date'] = pd.to_datetime(df_customers['signup_date'])
df_customers['days_since_signup'] = (pd.Timestamp.now() - df_customers['signup_date']).dt.days

print("\nCustomer tenure:")
print(df_customers[['customer_id', 'signup_date', 'days_since_signup']].head(10))

# %%
# Filter by date range
start_date = '2024-03-01'
end_date = '2024-06-30'

q2_sales = df_sales[(df_sales['date'] >= start_date) & (df_sales['date'] <= end_date)]
print(f"\nQ2 2024 sales: {len(q2_sales)} transactions")
print(f"Total Q2 revenue: ${q2_sales['total_amount'].sum():,.2f}")

# %%
# Group by time periods
monthly_revenue = df_sales.groupby(df_sales['date'].dt.to_period('M'))['total_amount'].sum()

plt.figure(figsize=(12, 6))
monthly_revenue.plot(kind='bar', color='steelblue')
plt.title('Monthly Revenue', fontsize=14, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Revenue ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 8. Handling Outliers
#
# Identify and deal with extreme values.

# %%
# Statistical summary to spot outliers
print("Sales amount statistics:")
print(df_sales['total_amount'].describe())

# %%
# Visualize distribution and outliers
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Histogram
ax1.hist(df_sales['total_amount'], bins=50, color='skyblue', edgecolor='black')
ax1.set_title('Distribution of Sales Amounts')
ax1.set_xlabel('Amount ($)')
ax1.set_ylabel('Frequency')

# Box plot
ax2.boxplot(df_sales['total_amount'])
ax2.set_title('Box Plot of Sales Amounts')
ax2.set_ylabel('Amount ($)')

plt.tight_layout()
plt.show()

# %%
# Identify outliers using IQR method
Q1 = df_sales['total_amount'].quantile(0.25)
Q3 = df_sales['total_amount'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"Q1: ${Q1:.2f}")
print(f"Q3: ${Q3:.2f}")
print(f"IQR: ${IQR:.2f}")
print(f"Lower bound: ${lower_bound:.2f}")
print(f"Upper bound: ${upper_bound:.2f}")

outliers = df_sales[(df_sales['total_amount'] < lower_bound) | 
                     (df_sales['total_amount'] > upper_bound)]
print(f"\nNumber of outliers: {len(outliers)}")

# %%
# Remove outliers
df_no_outliers = df_sales[(df_sales['total_amount'] >= lower_bound) & 
                           (df_sales['total_amount'] <= upper_bound)]
print(f"Original size: {len(df_sales)}")
print(f"After removing outliers: {len(df_no_outliers)}")

# %%
# Alternative: Cap outliers instead of removing
df_capped = df_sales.copy()
df_capped['total_amount'] = df_capped['total_amount'].clip(lower=lower_bound, upper=upper_bound)

print("Outliers capped at bounds")
print(f"Max value before: ${df_sales['total_amount'].max():.2f}")
print(f"Max value after: ${df_capped['total_amount'].max():.2f}")

# %% [markdown]
# ## 9. Standardizing and Normalizing Data

# %%
# Z-score standardization
df_customers['ltv_zscore'] = (df_customers['lifetime_value'] - df_customers['lifetime_value'].mean()) / df_customers['lifetime_value'].std()

print("Standardized lifetime value:")
print(df_customers[['customer_id', 'lifetime_value', 'ltv_zscore']].head(10))

# %%
# Min-Max normalization (0 to 1)
df_customers['ltv_normalized'] = ((df_customers['lifetime_value'] - df_customers['lifetime_value'].min()) / 
                                   (df_customers['lifetime_value'].max() - df_customers['lifetime_value'].min()))

print("\nNormalized lifetime value:")
print(df_customers[['customer_id', 'lifetime_value', 'ltv_normalized']].head(10))

# %% [markdown]
# ## 10. Complete Data Cleaning Pipeline
#
# Putting it all together!

# %%
def clean_survey_data(df):
    """
    Complete data cleaning pipeline for survey data
    """
    print("Starting data cleaning pipeline...")
    print(f"Initial shape: {df.shape}")
    
    # Step 1: Remove complete duplicates
    df = df.drop_duplicates()
    print(f"After removing duplicates: {df.shape}")
    
    # Step 2: Handle missing values
    # Fill categorical columns
    df['age_group'] = df['age_group'].fillna('Not specified')
    df['gender'] = df['gender'].fillna('Not specified')
    df['comments'] = df['comments'].fillna('No comment')
    
    # Fill numeric columns with median
    df['satisfaction_score'] = df['satisfaction_score'].fillna(df['satisfaction_score'].median())
    
    # Drop rows with missing critical fields
    df = df.dropna(subset=['product_quality', 'customer_service', 'would_recommend'])
    print(f"After handling missing values: {df.shape}")
    
    # Step 3: Standardize text fields
    df['region'] = df['region'].str.upper()
    df['would_recommend'] = df['would_recommend'].str.upper()
    
    # Step 4: Convert data types
    df['satisfaction_score'] = df['satisfaction_score'].astype(int)
    
    # Step 5: Create derived fields
    df['is_satisfied'] = df['satisfaction_score'] >= 4
    df['submission_month'] = df['submission_date'].dt.to_period('M')
    
    print(f"Final shape: {df.shape}")
    print("\nCleaning complete!")
    
    return df

# %%
# Apply cleaning pipeline
df_survey_clean = clean_survey_data(df_survey.copy())

print("\nCleaned data sample:")
print(df_survey_clean.head(10))

# %%
# Verify cleaning results
print("\nMissing values after cleaning:")
print(df_survey_clean.isnull().sum())

# %%
# Analyze cleaned data
print("\nSatisfaction distribution:")
print(df_survey_clean['satisfaction_score'].value_counts().sort_index())

print("\nRecommendation rate:")
print(df_survey_clean['would_recommend'].value_counts())

# %%
# Visualize cleaned data
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Satisfaction scores
df_survey_clean['satisfaction_score'].value_counts().sort_index().plot(kind='bar', ax=axes[0, 0], color='steelblue')
axes[0, 0].set_title('Satisfaction Score Distribution')
axes[0, 0].set_xlabel('Score')
axes[0, 0].set_ylabel('Count')

# Recommendation
df_survey_clean['would_recommend'].value_counts().plot(kind='pie', ax=axes[0, 1], autopct='%1.1f%%')
axes[0, 1].set_title('Would Recommend?')

# Age group
df_survey_clean['age_group'].value_counts().plot(kind='barh', ax=axes[1, 0], color='coral')
axes[1, 0].set_title('Responses by Age Group')
axes[1, 0].set_xlabel('Count')

# Region
df_survey_clean['region'].value_counts().plot(kind='bar', ax=axes[1, 1], color='teal')
axes[1, 1].set_title('Responses by Region')
axes[1, 1].set_xlabel('Region')
axes[1, 1].set_ylabel('Count')

plt.tight_layout()
plt.show()

# %% [markdown]
# ## Practice Exercise
#
# Clean the web traffic dataset!

# %%
# Load web traffic data
df_traffic = pd.read_csv('../datasets/web_traffic.csv')
print("Web traffic data:")
print(df_traffic.head())
print(f"\nShape: {df_traffic.shape}")
print("\nMissing values:")
print(df_traffic.isnull().sum())

# %%
# Exercise: Create cleaning pipeline
# 1. Convert timestamp to datetime
df_traffic['timestamp'] = pd.to_datetime(df_traffic['timestamp'])

# 2. Extract date components
df_traffic['hour'] = df_traffic['timestamp'].dt.hour
df_traffic['day_of_week'] = df_traffic['timestamp'].dt.day_name()

# 3. Categorize session duration
def categorize_session(duration):
    if duration < 60:
        return 'Short'
    elif duration < 300:
        return 'Medium'
    else:
        return 'Long'

df_traffic['session_category'] = df_traffic['session_duration_sec'].apply(categorize_session)

# 4. Analyze
print("\nTraffic by device type:")
print(df_traffic['device_type'].value_counts())

print("\nConversion rate by device:")
conversion_by_device = df_traffic.groupby('device_type')['conversion'].mean() * 100
print(conversion_by_device.round(2))

# %%
# Visualize traffic patterns
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Traffic by hour
hourly_traffic = df_traffic.groupby('hour').size()
ax1.plot(hourly_traffic.index, hourly_traffic.values, marker='o', linewidth=2)
ax1.set_title('Traffic by Hour of Day')
ax1.set_xlabel('Hour')
ax1.set_ylabel('Number of Visits')
ax1.grid(True, alpha=0.3)

# Conversion by traffic source
conversion_by_source = df_traffic.groupby('traffic_source')['conversion'].mean() * 100
conversion_by_source.plot(kind='barh', ax=ax2, color='coral')
ax2.set_title('Conversion Rate by Traffic Source')
ax2.set_xlabel('Conversion Rate (%)')

plt.tight_layout()
plt.show()

# %% [markdown]
# ## Summary
#
# In this module, you learned:
#
# ✓ **Identifying Missing Data**: Find and visualize missing values  
# ✓ **Handling Missing Data**: Drop, fill, or interpolate  
# ✓ **Removing Duplicates**: Clean duplicate records  
# ✓ **Data Type Conversion**: Ensure correct types  
# ✓ **String Operations**: Clean and manipulate text  
# ✓ **Date/Time Operations**: Parse and extract date components  
# ✓ **Handling Outliers**: Identify and treat extreme values  
# ✓ **Normalization**: Scale data for analysis  
# ✓ **Complete Pipeline**: Put it all together
#
# ### Quick Reference
#
# ```python
# # Missing data
# df.isnull().sum()
# df.dropna()
# df.fillna(value)
#
# # Duplicates
# df.duplicated()
# df.drop_duplicates()
#
# # Type conversion
# pd.to_datetime()
# pd.to_numeric()
# df['col'].astype('category')
#
# # String operations
# df['col'].str.lower()
# df['col'].str.strip()
# df['col'].str.replace()
# df['col'].str.contains()
#
# # Date operations
# df['date'].dt.year
# df['date'].dt.month
# df['date'].dt.day_name()
# ```
#
# Next up: **Module 6 - Automating Data Pipelines**!

