# %% [markdown]
# # Module 1: Python Quick Start
#
# Welcome to Python Data Analysis! In this module, we'll cover the essential Python fundamentals you need to get started with data analysis.
#
# ## Learning Objectives
# - Understand basic Python data types
# - Work with variables and operators
# - Use lists and dictionaries
# - Apply control flow (if/else, loops)
# - Compare Python to Excel operations

# %% [markdown]
# ## 1. Variables and Data Types
#
# In Python, variables store values. Unlike Excel cells, you give them meaningful names.

# %%
# Numbers (integers and floats)
quantity = 100
price = 29.99
total = quantity * price

print(f"Quantity: {quantity}")
print(f"Price: ${price}")
print(f"Total: ${total}")
print(f"Type of total: {type(total)}")

# %%
# Strings (text)
product_name = "Laptop"
customer_name = "John Smith"
greeting = f"Hello, {customer_name}! You ordered a {product_name}."

print(greeting)
print(f"Product name in uppercase: {product_name.upper()}")
print(f"Length of customer name: {len(customer_name)}")

# %%
# Booleans (True/False)
is_premium_customer = True
has_discount = False
in_stock = True

print(f"Premium customer: {is_premium_customer}")
print(f"Eligible for purchase: {in_stock and not has_discount}")

# %% [markdown]
# ### Excel Comparison
#
# | Excel | Python |
# |-------|--------|
# | Cell A1 = 100 | `quantity = 100` |
# | =A1*B1 | `total = quantity * price` |
# | =UPPER(A1) | `product_name.upper()` |
# | =LEN(A1) | `len(customer_name)` |
# | =IF(A1>100, "Yes", "No") | `"Yes" if quantity > 100 else "No"` |

# %% [markdown]
# ## 2. Lists - Collections of Items
#
# Lists are like a column in Excel, but more flexible.

# %%
# Creating a list
sales_amounts = [1200, 1500, 980, 2100, 1750]
regions = ["North", "South", "East", "West", "Central"]

print("Sales amounts:", sales_amounts)
print("Regions:", regions)

# %%
# Accessing list items (indexing starts at 0!)
print(f"First sale: ${sales_amounts[0]}")
print(f"Last sale: ${sales_amounts[-1]}")
print(f"First three sales: {sales_amounts[0:3]}")

# %%
# Common list operations
sales_amounts.append(1300)  # Add to end
print(f"After adding new sale: {sales_amounts}")

total_sales = sum(sales_amounts)
average_sales = total_sales / len(sales_amounts)
max_sale = max(sales_amounts)
min_sale = min(sales_amounts)

print(f"Total sales: ${total_sales}")
print(f"Average sales: ${average_sales:.2f}")
print(f"Maximum sale: ${max_sale}")
print(f"Minimum sale: ${min_sale}")

# %% [markdown]
# ## 3. Dictionaries - Key-Value Pairs
#
# Dictionaries are like a row in Excel, with column headers as keys.

# %%
# Creating a dictionary
customer = {
    "name": "Sarah Johnson",
    "customer_id": "CUST0123",
    "email": "sarah.johnson@email.com",
    "total_purchases": 15,
    "is_premium": True
}

print(customer)

# %%
# Accessing dictionary values
print(f"Customer name: {customer['name']}")
print(f"Email: {customer['email']}")
print(f"Total purchases: {customer['total_purchases']}")

# %%
# Adding/updating values
customer['phone'] = '555-1234'
customer['total_purchases'] = 16  # Update existing value

print("\nUpdated customer:")
for key, value in customer.items():
    print(f"  {key}: {value}")

# %% [markdown]
# ## 4. Control Flow - If/Else Statements
#
# Make decisions in your code based on conditions.

# %%
# Simple if/else
order_amount = 150

if order_amount > 100:
    discount = 0.10
    print(f"Order qualifies for 10% discount!")
else:
    discount = 0
    print(f"Order does not qualify for discount.")

final_amount = order_amount * (1 - discount)
print(f"Final amount: ${final_amount:.2f}")

# %%
# Multiple conditions with elif
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score} = Grade: {grade}")

# %%
# Complex conditions
age = 28
has_license = True
is_insured = True

can_rent_car = age >= 21 and has_license and is_insured

if can_rent_car:
    print("✓ Customer can rent a car")
else:
    print("✗ Customer cannot rent a car")

# %% [markdown]
# ## 5. Loops - Repeating Actions
#
# Loops let you process multiple items efficiently.

# %%
# For loop - iterate through a list
products = ["Laptop", "Mouse", "Keyboard", "Monitor"]

print("Products in stock:")
for product in products:
    print(f"  - {product}")

# %%
# Loop with calculations
monthly_sales = [15000, 18000, 16500, 19200, 17800, 20000]

print("Monthly Sales Analysis:")
for month, sales in enumerate(monthly_sales, start=1):
    print(f"  Month {month}: ${sales:,}")

print(f"\nTotal for 6 months: ${sum(monthly_sales):,}")
print(f"Average monthly sales: ${sum(monthly_sales)/len(monthly_sales):,.2f}")

# %%
# Loop with conditions
temperatures = [72, 65, 80, 95, 68, 71, 88]

print("Hot days (>85°F):")
for i, temp in enumerate(temperatures, start=1):
    if temp > 85:
        print(f"  Day {i}: {temp}°F")

# %% [markdown]
# ## 6. List Comprehensions - Compact Loops
#
# A Pythonic way to create new lists from existing ones.

# %%
# Traditional way
prices = [29.99, 49.99, 19.99, 99.99, 39.99]
prices_with_tax = []

for price in prices:
    prices_with_tax.append(price * 1.08)

print("Traditional way:", prices_with_tax)

# %%
# List comprehension way (more Pythonic)
prices_with_tax = [price * 1.08 for price in prices]
print("List comprehension:", prices_with_tax)

# %%
# With conditions
sales = [100, 250, 450, 180, 520, 90, 300]
large_sales = [sale for sale in sales if sale >= 200]

print("Large sales (≥$200):", large_sales)

# %% [markdown]
# ## Practice Exercise
#
# Let's apply what we've learned!

# %%
# Sample sales data for one week
weekly_sales = {
    'Monday': 1250,
    'Tuesday': 1580,
    'Wednesday': 1420,
    'Thursday': 1890,
    'Friday': 2150,
    'Saturday': 2400,
    'Sunday': 1980
}

# Task 1: Calculate total weekly sales
total = sum(weekly_sales.values())
print(f"Total weekly sales: ${total:,}")

# Task 2: Calculate average daily sales
average = total / len(weekly_sales)
print(f"Average daily sales: ${average:,.2f}")

# Task 3: Find best and worst days
best_day = max(weekly_sales, key=weekly_sales.get)
worst_day = min(weekly_sales, key=weekly_sales.get)
print(f"Best day: {best_day} (${weekly_sales[best_day]:,})")
print(f"Worst day: {worst_day} (${weekly_sales[worst_day]:,})")

# Task 4: Find days above average
print("\nDays above average:")
for day, sales in weekly_sales.items():
    if sales > average:
        print(f"  {day}: ${sales:,}")

# %% [markdown]
# ## Summary
#
# In this module, you learned:
#
# ✓ **Variables and Data Types**: Storing numbers, text, and boolean values  
# ✓ **Lists**: Working with collections of items  
# ✓ **Dictionaries**: Organizing data with key-value pairs  
# ✓ **Control Flow**: Making decisions with if/else statements  
# ✓ **Loops**: Iterating through data efficiently  
# ✓ **List Comprehensions**: Creating lists in a Pythonic way
#
# ### Key Takeaways for Excel Users
#
# - Python variables = Excel named cells
# - Python lists = Excel columns
# - Python dictionaries = Excel rows with headers
# - Python if/else = Excel IF() function
# - Python loops = Dragging formulas down in Excel (but more powerful!)
#
# Next up: **Module 2 - Introduction to Pandas** where we'll work with real datasets!

