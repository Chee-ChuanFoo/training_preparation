"""
Script to generate sample datasets for Python Data Analysis course
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# =====================================
# 1. Sales Data
# =====================================
print("Generating sales_data.csv...")

n_sales = 1000
start_date = datetime(2024, 1, 1)

sales_data = {
    'transaction_id': [f'TXN{str(i).zfill(6)}' for i in range(1, n_sales + 1)],
    'date': [start_date + timedelta(days=random.randint(0, 270)) for _ in range(n_sales)],
    'product_id': [f'PRD{random.randint(1, 50):03d}' for _ in range(n_sales)],
    'customer_id': [f'CUST{random.randint(1, 200):04d}' for _ in range(n_sales)],
    'quantity': np.random.randint(1, 10, n_sales),
    'unit_price': np.round(np.random.uniform(10, 500, n_sales), 2),
    'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_sales),
    'sales_rep': np.random.choice(['John Smith', 'Mary Johnson', 'David Lee', 'Sarah Wilson', 
                                    'Michael Brown', 'Jennifer Davis', 'Robert Garcia', 'Lisa Martinez'], n_sales),
    'payment_method': np.random.choice(['Credit Card', 'Cash', 'Debit Card', 'PayPal', 'Wire Transfer'], 
                                       n_sales, p=[0.4, 0.2, 0.25, 0.1, 0.05])
}

df_sales = pd.DataFrame(sales_data)
df_sales['total_amount'] = df_sales['quantity'] * df_sales['unit_price']
df_sales = df_sales.sort_values('date').reset_index(drop=True)
df_sales.to_csv('datasets/sales_data.csv', index=False)
print(f"  Created {len(df_sales)} sales records")

# =====================================
# 2. Customer Data
# =====================================
print("Generating customer_data.csv...")

n_customers = 200
first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
               'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
               'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
              'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
              'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White']

customer_data = {
    'customer_id': [f'CUST{i:04d}' for i in range(1, n_customers + 1)],
    'first_name': [random.choice(first_names) for _ in range(n_customers)],
    'last_name': [random.choice(last_names) for _ in range(n_customers)],
    'email': [f"{random.choice(first_names).lower()}.{random.choice(last_names).lower()}@email.com" 
              for _ in range(n_customers)],
    'phone': [f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}" 
              for _ in range(n_customers)],
    'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                              'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'], n_customers),
    'state': np.random.choice(['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'FL', 'OH', 'NC', 'GA'], n_customers),
    'signup_date': [start_date - timedelta(days=random.randint(0, 730)) for _ in range(n_customers)],
    'customer_segment': np.random.choice(['Premium', 'Standard', 'Basic'], n_customers, p=[0.2, 0.5, 0.3]),
    'total_purchases': np.random.randint(1, 50, n_customers),
    'lifetime_value': np.round(np.random.uniform(100, 10000, n_customers), 2)
}

df_customers = pd.DataFrame(customer_data)
df_customers.to_csv('datasets/customer_data.csv', index=False)
print(f"  Created {len(df_customers)} customer records")

# =====================================
# 3. Product Catalog
# =====================================
print("Generating product_catalog.csv...")

product_categories = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smart Watch', 'Camera'],
    'Home & Garden': ['Furniture', 'Lighting', 'Decor', 'Kitchen Appliances', 'Bedding'],
    'Sports': ['Fitness Equipment', 'Outdoor Gear', 'Athletic Wear', 'Sports Accessories'],
    'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Children\'s Books'],
    'Clothing': ['Men\'s Wear', 'Women\'s Wear', 'Accessories', 'Shoes']
}

products = []
product_id = 1

for category, subcategories in product_categories.items():
    for subcategory in subcategories:
        for i in range(2):
            products.append({
                'product_id': f'PRD{product_id:03d}',
                'product_name': f'{subcategory} {chr(65+i)}',
                'category': category,
                'subcategory': subcategory,
                'cost_price': round(random.uniform(10, 400), 2),
                'retail_price': round(random.uniform(15, 500), 2),
                'stock_quantity': random.randint(0, 500),
                'supplier': random.choice(['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D']),
                'weight_kg': round(random.uniform(0.1, 5.0), 2),
                'is_active': random.choice([True, True, True, False])  # 75% active
            })
            product_id += 1

df_products = pd.DataFrame(products)
df_products['profit_margin'] = ((df_products['retail_price'] - df_products['cost_price']) / 
                                 df_products['retail_price'] * 100).round(2)
df_products.to_csv('datasets/product_catalog.csv', index=False)
print(f"  Created {len(df_products)} product records")

# =====================================
# 4. Web Traffic Data
# =====================================
print("Generating web_traffic.csv...")

n_visits = 2000
start_datetime = datetime(2024, 1, 1, 0, 0, 0)

pages = ['/home', '/products', '/about', '/contact', '/checkout', '/cart', 
         '/product/electronics', '/product/clothing', '/product/sports', '/blog']

web_traffic = {
    'visit_id': [f'VISIT{i:06d}' for i in range(1, n_visits + 1)],
    'timestamp': [start_datetime + timedelta(hours=random.randint(0, 6480)) for _ in range(n_visits)],
    'page_url': np.random.choice(pages, n_visits),
    'session_duration_sec': np.random.randint(10, 3600, n_visits),
    'device_type': np.random.choice(['Desktop', 'Mobile', 'Tablet'], n_visits, p=[0.5, 0.4, 0.1]),
    'browser': np.random.choice(['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera'], 
                                n_visits, p=[0.5, 0.2, 0.15, 0.1, 0.05]),
    'traffic_source': np.random.choice(['Organic Search', 'Direct', 'Social Media', 'Email', 'Paid Ads'], 
                                       n_visits, p=[0.35, 0.25, 0.2, 0.1, 0.1]),
    'country': np.random.choice(['USA', 'Canada', 'UK', 'Germany', 'France', 'Japan', 'Australia'], n_visits),
    'bounce': np.random.choice([True, False], n_visits, p=[0.4, 0.6]),
    'conversion': np.random.choice([True, False], n_visits, p=[0.05, 0.95])
}

df_traffic = pd.DataFrame(web_traffic)
df_traffic['page_views'] = np.random.randint(1, 20, n_visits)
df_traffic = df_traffic.sort_values('timestamp').reset_index(drop=True)
df_traffic.to_csv('datasets/web_traffic.csv', index=False)
print(f"  Created {len(df_traffic)} web visit records")

# =====================================
# 5. Survey Results (with missing data)
# =====================================
print("Generating survey_results.csv...")

n_responses = 500

survey_questions = {
    'response_id': [f'RESP{i:05d}' for i in range(1, n_responses + 1)],
    'submission_date': [start_date + timedelta(days=random.randint(0, 90)) for _ in range(n_responses)],
    'age_group': np.random.choice(['18-25', '26-35', '36-45', '46-55', '56-65', '65+', None], 
                                  n_responses, p=[0.15, 0.25, 0.23, 0.17, 0.1, 0.05, 0.05]),
    'gender': np.random.choice(['Male', 'Female', 'Other', 'Prefer not to say', None], 
                               n_responses, p=[0.45, 0.45, 0.02, 0.05, 0.03]),
    'satisfaction_score': np.random.choice([1, 2, 3, 4, 5, None], n_responses, p=[0.05, 0.1, 0.2, 0.35, 0.25, 0.05]),
    'product_quality': np.random.choice(['Poor', 'Fair', 'Good', 'Very Good', 'Excellent', None], 
                                       n_responses, p=[0.03, 0.07, 0.25, 0.35, 0.25, 0.05]),
    'customer_service': np.random.choice(['Poor', 'Fair', 'Good', 'Very Good', 'Excellent', None], 
                                        n_responses, p=[0.02, 0.08, 0.3, 0.32, 0.23, 0.05]),
    'would_recommend': np.random.choice(['Yes', 'No', 'Maybe', None], n_responses, p=[0.6, 0.15, 0.2, 0.05]),
    'annual_income': np.random.choice(['<$25k', '$25k-$50k', '$50k-$75k', '$75k-$100k', '>$100k', None], 
                                     n_responses, p=[0.1, 0.2, 0.25, 0.22, 0.15, 0.08]),
    'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_responses),
    'comments': [random.choice([
        'Great service!', 'Could be better', 'Very satisfied', 'Had some issues', 
        'Excellent experience', 'Average', 'Not what I expected', None, None, None
    ]) for _ in range(n_responses)]
}

df_survey = pd.DataFrame(survey_questions)
df_survey = df_survey.sort_values('submission_date').reset_index(drop=True)
df_survey.to_csv('datasets/survey_results.csv', index=False)
print(f"  Created {len(df_survey)} survey responses (with intentional missing data)")

print("\n✓ All datasets generated successfully!")
print("\nDataset Summary:")
print(f"  - sales_data.csv: {len(df_sales)} rows")
print(f"  - customer_data.csv: {len(df_customers)} rows")
print(f"  - product_catalog.csv: {len(df_products)} rows")
print(f"  - web_traffic.csv: {len(df_traffic)} rows")
print(f"  - survey_results.csv: {len(df_survey)} rows (with missing values)")

