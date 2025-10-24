# %% [markdown]
# # Comprehensive Practice Exercises
#
# This notebook contains hands-on exercises covering all modules from the course.
# Try to complete them on your own before checking the solutions!
#
# ## Instructions
# 1. Read each exercise carefully
# 2. Write your code in the empty cells
# 3. Run your code to verify it works
# 4. Compare with the solution notebook when done

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
# Create a list of monthly revenue values and calculate:
# - Total revenue
# - Average monthly revenue
# - The highest and lowest months
# - How many months exceeded $20,000

# %%
# Your code here
monthly_revenue = [18000, 22000, 19500, 25000, 21000, 23500, 26000, 24000, 22500, 27000, 29000, 31000]

# Calculate statistics


# %% [markdown]
# ### Task B: Dictionary Operations
# Create a dictionary for a product with: name, price, quantity, category
# Then calculate the total value (price * quantity)

# %%
# Your code here


# %% [markdown]
# ## Exercise 2: Loading and Exploring Data (10 points)
#
# Load the sales data and answer these questions:
# 1. How many transactions are there?
# 2. What is the date range of the data?
# 3. How many unique customers made purchases?
# 4. What are the top 3 payment methods used?

# %%
# Load the data
# df_sales = pd.read_csv('../datasets/sales_data.csv', parse_dates=['date'])

# Your analysis here


# %% [markdown]
# ## Exercise 3: Filtering and Selection (15 points)
#
# Using the sales data:
# 1. Find all transactions over $1,500
# 2. Find all transactions from the "North" or "South" region
# 3. Find transactions over $1,000 AND from "East" region
# 4. Display only the date, region, and total_amount columns

# %%
# Your code here


# %% [markdown]
# ## Exercise 4: Groupby and Aggregation (20 points)
#
# Analyze sales performance:
# 1. Calculate total sales by region
# 2. Calculate average transaction amount by payment method
# 3. Count number of transactions per sales representative
# 4. Create a summary showing: total sales, average sale, and transaction count by region

# %%
# Your code here


# %% [markdown]
# ## Exercise 5: Data Visualization (20 points)
#
# Create the following visualizations:
# 1. Bar chart: Total sales by region
# 2. Line chart: Daily sales trend over time
# 3. Pie chart: Distribution of payment methods
# 4. Histogram: Distribution of transaction amounts

# %%
# Visualization 1: Bar chart
# Your code here


# %%
# Visualization 2: Line chart
# Your code here


# %%
# Visualization 3: Pie chart
# Your code here


# %%
# Visualization 4: Histogram
# Your code here


# %% [markdown]
# ## Exercise 6: Merging Data (15 points)
#
# 1. Load the customer data
# 2. Merge it with sales data on customer_id
# 3. Calculate total sales by customer segment
# 4. Find the top 5 customers by total purchase amount

# %%
# Load customer data
# df_customers = pd.read_csv('../datasets/customer_data.csv')

# Your code here


# %% [markdown]
# ## Exercise 7: Data Cleaning (20 points)
#
# Load the survey data and:
# 1. Check for missing values in each column
# 2. Fill missing satisfaction_score with the median
# 3. Fill missing age_group with "Not specified"
# 4. Remove rows where would_recommend is missing
# 5. Show the before and after counts

# %%
# Load survey data
# df_survey = pd.read_csv('../datasets/survey_results.csv', parse_dates=['submission_date'])

# Your code here


# %% [markdown]
# ## Exercise 8: Date/Time Analysis (15 points)
#
# Using sales data:
# 1. Extract month and day_of_week from date
# 2. Calculate total sales by month
# 3. Calculate average sales by day of week
# 4. Visualize monthly sales as a line chart

# %%
# Your code here


# %% [markdown]
# ## Exercise 9: Pivot Tables (15 points)
#
# Create pivot tables showing:
# 1. Sales amount by region (rows) and payment method (columns)
# 2. Count of transactions by sales_rep (rows) and region (columns)
# 3. Average transaction amount by quarter (rows) and region (columns)

# %%
# Your code here


# %% [markdown]
# ## Exercise 10: Comprehensive Analysis (20 points)
#
# ### Business Question:
# Your manager wants to know: "Which sales representatives are performing best, and in which regions?"
#
# Create an analysis that includes:
# 1. Total sales per sales rep
# 2. Average transaction size per sales rep
# 3. Number of transactions per sales rep
# 4. A breakdown of each rep's sales by region
# 5. A visualization showing the top 5 reps by total sales

# %%
# Your comprehensive analysis here


# %% [markdown]
# ## Challenge Exercise: Mini Dashboard (Bonus 30 points)
#
# Create a professional-looking dashboard with 4 visualizations:
# 1. Key metrics (total sales, avg transaction, etc.) as text
# 2. Sales by region (bar chart)
# 3. Sales trend over time (line chart)
# 4. Payment method distribution (pie chart)
#
# Use subplots to arrange them nicely!

# %%
# Your dashboard code here


# %% [markdown]
# ## Challenge Exercise: Custom Function (Bonus 20 points)
#
# Create a reusable function that takes a DataFrame and generates a sales report.
#
# The function should:
# - Accept a DataFrame as input
# - Calculate key metrics (total, average, count)
# - Return a formatted summary as a string
# - Handle errors gracefully

# %%
def generate_sales_summary(df):
    """
    Generate a sales summary report
    
    Parameters:
    - df: DataFrame with sales data
    
    Returns:
    - str: Formatted summary report
    """
    # Your code here
    pass

# Test your function
# print(generate_sales_summary(df_sales))


# %% [markdown]
# ## Self-Assessment
#
# Rate your confidence (1-5) for each skill:
#
# - [ ] Python basics (lists, dictionaries, loops): ___/5
# - [ ] Loading and exploring data: ___/5
# - [ ] Filtering and selecting data: ___/5
# - [ ] GroupBy operations: ___/5
# - [ ] Data visualization: ___/5
# - [ ] Merging datasets: ___/5
# - [ ] Data cleaning: ___/5
# - [ ] Date/time operations: ___/5
# - [ ] Pivot tables: ___/5
# - [ ] Creating functions: ___/5
#
# **Next Steps:**
# - Areas where you scored 1-2: Review the corresponding module
# - Areas where you scored 3: Practice more with similar exercises
# - Areas where you scored 4-5: Great! Try more advanced topics
#
# ---
#
# **Great job working through these exercises! 🎉**
#
# Remember: The best way to learn is by doing. Keep practicing with real datasets!

