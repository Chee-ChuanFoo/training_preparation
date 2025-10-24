# %% [markdown]
# # Module 6: Automating Data Pipelines
#
# Learn to automate your data analysis workflows and create scheduled reports!
#
# ## Learning Objectives
# - Convert notebooks to Python scripts
# - Create reusable functions
# - Build ETL (Extract, Transform, Load) pipelines
# - Schedule automated tasks
# - Generate automated reports
# - Best practices for production code

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

print("Libraries loaded!")
print(f"Current directory: {os.getcwd()}")

# %% [markdown]
# ## 1. From Notebook to Script
#
# Jupyter notebooks are great for exploration, but scripts are better for automation.

# %% [markdown]
# ### Key Differences
#
# **Jupyter Notebooks:**
# - Interactive exploration
# - Mix code, visualizations, and narrative
# - Cell-by-cell execution
# - Great for analysis and presentation
#
# **Python Scripts:**
# - Automated execution
# - Run start to finish
# - Can be scheduled
# - Better for production pipelines

# %% [markdown]
# ## 2. Creating Reusable Functions
#
# Functions make your code modular and reusable.

# %%
# Simple function example
def calculate_revenue(quantity, price):
    """Calculate total revenue from quantity and price"""
    return quantity * price

# Test the function
result = calculate_revenue(100, 29.99)
print(f"Revenue: ${result:,.2f}")

# %%
# Function with data cleaning
def clean_customer_data(df):
    """
    Clean customer data
    
    Parameters:
    - df: pandas DataFrame with customer data
    
    Returns:
    - Cleaned DataFrame
    """
    # Make a copy to avoid modifying original
    df_clean = df.copy()
    
    # Standardize text fields
    df_clean['state'] = df_clean['state'].str.upper()
    
    # Handle missing values
    df_clean['phone'] = df_clean['phone'].fillna('Not provided')
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates(subset=['customer_id'])
    
    return df_clean

# %%
# Function with analysis
def analyze_sales_by_region(df):
    """
    Analyze sales by region
    
    Parameters:
    - df: pandas DataFrame with sales data
    
    Returns:
    - Dictionary with analysis results
    """
    analysis = {
        'total_by_region': df.groupby('region')['total_amount'].sum().to_dict(),
        'avg_by_region': df.groupby('region')['total_amount'].mean().to_dict(),
        'count_by_region': df.groupby('region').size().to_dict(),
        'top_region': df.groupby('region')['total_amount'].sum().idxmax(),
        'total_revenue': df['total_amount'].sum()
    }
    
    return analysis

# %%
# Test the analysis function
df_sales = pd.read_csv('../datasets/sales_data.csv', parse_dates=['date'])
results = analyze_sales_by_region(df_sales)

print("Sales Analysis Results:")
print(f"Total Revenue: ${results['total_revenue']:,.2f}")
print(f"Top Region: {results['top_region']}")
print("\nRevenue by Region:")
for region, revenue in results['total_by_region'].items():
    print(f"  {region}: ${revenue:,.2f}")

# %% [markdown]
# ## 3. Building an ETL Pipeline
#
# ETL = Extract, Transform, Load

# %%
def extract_sales_data(filepath):
    """
    Extract: Load sales data from CSV
    """
    print(f"Extracting data from {filepath}...")
    df = pd.read_csv(filepath, parse_dates=['date'])
    print(f"  Loaded {len(df)} records")
    return df

def transform_sales_data(df):
    """
    Transform: Clean and enrich sales data
    """
    print("Transforming data...")
    
    # Create a copy
    df_transformed = df.copy()
    
    # Add time features
    df_transformed['year'] = df_transformed['date'].dt.year
    df_transformed['month'] = df_transformed['date'].dt.month
    df_transformed['quarter'] = df_transformed['date'].dt.quarter
    df_transformed['day_of_week'] = df_transformed['date'].dt.day_name()
    
    # Categorize sales
    def categorize_sale(amount):
        if amount >= 1000:
            return 'High'
        elif amount >= 500:
            return 'Medium'
        else:
            return 'Low'
    
    df_transformed['sale_category'] = df_transformed['total_amount'].apply(categorize_sale)
    
    # Calculate commission (5%)
    df_transformed['commission'] = df_transformed['total_amount'] * 0.05
    
    # Standardize region names
    df_transformed['region'] = df_transformed['region'].str.upper()
    
    print(f"  Transformation complete: {len(df_transformed)} records")
    return df_transformed

def load_sales_data(df, output_path):
    """
    Load: Save processed data
    """
    print(f"Loading data to {output_path}...")
    df.to_csv(output_path, index=False)
    print(f"  Saved {len(df)} records")
    return True

# %%
# Run the ETL pipeline
def run_sales_etl_pipeline(input_file, output_file):
    """
    Complete ETL pipeline for sales data
    """
    print("=" * 50)
    print("STARTING ETL PIPELINE")
    print("=" * 50)
    
    try:
        # Extract
        df_raw = extract_sales_data(input_file)
        
        # Transform
        df_transformed = transform_sales_data(df_raw)
        
        # Load
        load_sales_data(df_transformed, output_file)
        
        print("\n" + "=" * 50)
        print("ETL PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 50)
        
        return df_transformed
        
    except Exception as e:
        print(f"\nERROR in ETL pipeline: {str(e)}")
        return None

# %%
# Execute the pipeline
df_processed = run_sales_etl_pipeline(
    '../datasets/sales_data.csv',
    '../datasets/sales_processed.csv'
)

if df_processed is not None:
    print("\nProcessed data sample:")
    print(df_processed.head())

# %% [markdown]
# ## 4. Generating Automated Reports

# %%
def generate_sales_report(df, report_date=None):
    """
    Generate a comprehensive sales report
    """
    if report_date is None:
        report_date = datetime.now().strftime('%Y-%m-%d')
    
    print("=" * 60)
    print(f"SALES REPORT - Generated on {report_date}")
    print("=" * 60)
    
    # Overall metrics
    print("\n📊 OVERALL METRICS")
    print("-" * 60)
    print(f"Total Revenue:        ${df['total_amount'].sum():>15,.2f}")
    print(f"Average Transaction:  ${df['total_amount'].mean():>15,.2f}")
    print(f"Total Transactions:   {len(df):>18,}")
    print(f"Unique Customers:     {df['customer_id'].nunique():>18,}")
    print(f"Unique Products:      {df['product_id'].nunique():>18,}")
    
    # Regional breakdown
    print("\n🌍 REGIONAL BREAKDOWN")
    print("-" * 60)
    regional_sales = df.groupby('region')['total_amount'].agg(['sum', 'mean', 'count'])
    regional_sales.columns = ['Total_Revenue', 'Avg_Transaction', 'Num_Transactions']
    regional_sales = regional_sales.sort_values('Total_Revenue', ascending=False)
    
    for region, row in regional_sales.iterrows():
        print(f"\n{region}:")
        print(f"  Total Revenue:     ${row['Total_Revenue']:,.2f}")
        print(f"  Avg Transaction:   ${row['Avg_Transaction']:,.2f}")
        print(f"  Transactions:      {int(row['Num_Transactions']):,}")
    
    # Top performers
    print("\n🏆 TOP PERFORMERS")
    print("-" * 60)
    
    # Top products
    top_products = df.groupby('product_id')['total_amount'].sum().nlargest(5)
    print("\nTop 5 Products by Revenue:")
    for i, (product, revenue) in enumerate(top_products.items(), 1):
        print(f"  {i}. {product}: ${revenue:,.2f}")
    
    # Top sales reps
    top_reps = df.groupby('sales_rep')['total_amount'].sum().nlargest(5)
    print("\nTop 5 Sales Representatives:")
    for i, (rep, revenue) in enumerate(top_reps.items(), 1):
        print(f"  {i}. {rep}: ${revenue:,.2f}")
    
    # Payment method analysis
    print("\n💳 PAYMENT METHOD ANALYSIS")
    print("-" * 60)
    payment_analysis = df.groupby('payment_method').agg({
        'total_amount': ['sum', 'count']
    })
    payment_analysis.columns = ['Total_Revenue', 'Num_Transactions']
    payment_analysis = payment_analysis.sort_values('Total_Revenue', ascending=False)
    
    for method, row in payment_analysis.iterrows():
        pct = (row['Total_Revenue'] / df['total_amount'].sum() * 100)
        print(f"{method}: ${row['Total_Revenue']:,.2f} ({pct:.1f}%)")
    
    # Time analysis
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        print("\n📅 TIME ANALYSIS")
        print("-" * 60)
        date_range = f"{df['date'].min().date()} to {df['date'].max().date()}"
        print(f"Date Range: {date_range}")
        
        if 'month' in df.columns:
            monthly = df.groupby('month')['total_amount'].sum()
            print(f"\nBest Month: Month {monthly.idxmax()} (${monthly.max():,.2f})")
            print(f"Worst Month: Month {monthly.idxmin()} (${monthly.min():,.2f})")
    
    print("\n" + "=" * 60)
    print("END OF REPORT")
    print("=" * 60)

# %%
# Generate report
generate_sales_report(df_processed)

# %% [markdown]
# ## 5. Creating Visualizations for Reports

# %%
def create_sales_dashboard(df, output_file='sales_dashboard.png'):
    """
    Create a visual dashboard for the sales report
    """
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Plot 1: Revenue by Region (Bar)
    ax1 = fig.add_subplot(gs[0, :2])
    region_sales = df.groupby('region')['total_amount'].sum().sort_values(ascending=False)
    ax1.bar(region_sales.index, region_sales.values, color='#2E86AB')
    ax1.set_title('Total Revenue by Region', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Revenue ($)')
    ax1.grid(axis='y', alpha=0.3)
    
    # Plot 2: Key Metrics (Text)
    ax2 = fig.add_subplot(gs[0, 2])
    ax2.axis('off')
    metrics_text = f"""
KEY METRICS

Total Revenue:
${df['total_amount'].sum():,.0f}

Avg Transaction:
${df['total_amount'].mean():,.0f}

Total Transactions:
{len(df):,}

Unique Customers:
{df['customer_id'].nunique():,}
"""
    ax2.text(0.1, 0.5, metrics_text, fontsize=12, verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='#F0F0F0', alpha=0.8))
    
    # Plot 3: Payment Methods (Pie)
    ax3 = fig.add_subplot(gs[1, 0])
    payment_counts = df['payment_method'].value_counts()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    ax3.pie(payment_counts.values, labels=payment_counts.index, autopct='%1.0f%%',
            colors=colors, textprops={'fontsize': 9})
    ax3.set_title('Payment Methods', fontsize=12, fontweight='bold')
    
    # Plot 4: Sales Trend (Line)
    ax4 = fig.add_subplot(gs[1, 1:])
    daily_sales = df.groupby('date')['total_amount'].sum().sort_index()
    ax4.plot(daily_sales.index, daily_sales.values, linewidth=2, color='#2ECC71')
    ax4.set_title('Daily Sales Trend', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Sales ($)')
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(True, alpha=0.3)
    
    # Plot 5: Top Products (Horizontal Bar)
    ax5 = fig.add_subplot(gs[2, :2])
    top_products = df.groupby('product_id')['total_amount'].sum().nlargest(10)
    ax5.barh(range(len(top_products)), top_products.values, color='coral')
    ax5.set_yticks(range(len(top_products)))
    ax5.set_yticklabels(top_products.index)
    ax5.set_xlabel('Revenue ($)')
    ax5.set_title('Top 10 Products by Revenue', fontsize=12, fontweight='bold')
    ax5.grid(axis='x', alpha=0.3)
    
    # Plot 6: Sales Distribution (Histogram)
    ax6 = fig.add_subplot(gs[2, 2])
    ax6.hist(df['total_amount'], bins=30, color='#9B59B6', edgecolor='black', alpha=0.7)
    ax6.axvline(df['total_amount'].mean(), color='red', linestyle='--', linewidth=2)
    ax6.set_xlabel('Amount ($)')
    ax6.set_ylabel('Frequency')
    ax6.set_title('Transaction Distribution', fontsize=12, fontweight='bold')
    
    plt.suptitle(f'SALES DASHBOARD - {datetime.now().strftime("%Y-%m-%d")}',
                 fontsize=18, fontweight='bold', y=0.98)
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Dashboard saved to: {output_file}")
    
    plt.show()

# %%
# Create dashboard
create_sales_dashboard(df_processed)

# %% [markdown]
# ## 6. Complete Automated Report Pipeline

# %%
def automated_report_pipeline(data_file, report_name='Daily_Sales_Report'):
    """
    Complete automated reporting pipeline
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print("\n" + "="*70)
    print(f"AUTOMATED REPORT PIPELINE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    try:
        # Step 1: Load and process data
        print("\n[1/4] Loading and processing data...")
        df = pd.read_csv(data_file, parse_dates=['date'])
        df = transform_sales_data(df)
        print(f"     ✓ Processed {len(df)} records")
        
        # Step 2: Generate text report
        print("\n[2/4] Generating text report...")
        report_file = f'{report_name}_{timestamp}.txt'
        
        # Redirect print output to file
        import sys
        original_stdout = sys.stdout
        with open(report_file, 'w') as f:
            sys.stdout = f
            generate_sales_report(df)
        sys.stdout = original_stdout
        print(f"     ✓ Report saved to: {report_file}")
        
        # Step 3: Generate visualizations
        print("\n[3/4] Creating dashboard...")
        dashboard_file = f'{report_name}_Dashboard_{timestamp}.png'
        create_sales_dashboard(df, dashboard_file)
        print(f"     ✓ Dashboard saved to: {dashboard_file}")
        
        # Step 4: Export processed data
        print("\n[4/4] Exporting processed data...")
        data_export = f'{report_name}_Data_{timestamp}.csv'
        df.to_csv(data_export, index=False)
        print(f"     ✓ Data exported to: {data_export}")
        
        print("\n" + "="*70)
        print("REPORT PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*70)
        print(f"\nGenerated files:")
        print(f"  1. {report_file}")
        print(f"  2. {dashboard_file}")
        print(f"  3. {data_export}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# %%
# Run the automated report
# automated_report_pipeline('../datasets/sales_data.csv')
# Commented out to avoid creating multiple files during training

# %% [markdown]
# ## 7. Scheduling Automation (Without Airflow)
#
# For beginners, we'll use simple scheduling methods.

# %% [markdown]
# ### Windows Task Scheduler
#
# ```
# 1. Create a batch file (run_report.bat):
#    ===================================
#    @echo off
#    cd C:\path\to\your\project
#    python report_script.py
#    pause
#    ===================================
#
# 2. Open Task Scheduler (search in Windows)
# 3. Click "Create Basic Task"
# 4. Name: "Daily Sales Report"
# 5. Trigger: Daily at 8:00 AM
# 6. Action: Start a program
# 7. Program: C:\path\to\run_report.bat
# 8. Finish
# ```

# %% [markdown]
# ### Mac/Linux Cron Job
#
# ```
# 1. Open terminal and type: crontab -e
#
# 2. Add this line (runs daily at 8 AM):
#    0 8 * * * cd /path/to/project && python report_script.py
#
# 3. Save and exit
#
# Cron syntax: minute hour day month day_of_week
# Examples:
# - 0 8 * * *        # Daily at 8 AM
# - 0 8 * * 1        # Every Monday at 8 AM
# - 0 8 1 * *        # First day of month at 8 AM
# - */30 * * * *     # Every 30 minutes
# ```

# %% [markdown]
# ## 8. Error Handling and Logging

# %%
import logging
from datetime import datetime

def setup_logging(log_file='pipeline.log'):
    """
    Set up logging for the pipeline
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getlogger(__name__)

def robust_etl_pipeline(input_file, output_file):
    """
    ETL pipeline with error handling and logging
    """
    logger = setup_logging()
    
    logger.info("="*50)
    logger.info("Starting ETL Pipeline")
    logger.info("="*50)
    
    try:
        # Extract
        logger.info(f"Extracting data from {input_file}")
        df = pd.read_csv(input_file, parse_dates=['date'])
        logger.info(f"Successfully loaded {len(df)} records")
        
        # Transform
        logger.info("Transforming data...")
        df = transform_sales_data(df)
        logger.info("Transformation complete")
        
        # Validate
        logger.info("Validating data...")
        assert len(df) > 0, "No data to process"
        assert 'total_amount' in df.columns, "Missing total_amount column"
        logger.info("Validation passed")
        
        # Load
        logger.info(f"Saving data to {output_file}")
        df.to_csv(output_file, index=False)
        logger.info("Data saved successfully")
        
        logger.info("="*50)
        logger.info("ETL Pipeline Completed Successfully")
        logger.info("="*50)
        
        return df
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return None
    except pd.errors.EmptyDataError:
        logger.error("Input file is empty")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None

# %% [markdown]
# ## 9. Configuration Management

# %%
# Create a configuration dictionary
config = {
    'data_sources': {
        'sales': '../datasets/sales_data.csv',
        'customers': '../datasets/customer_data.csv',
        'products': '../datasets/product_catalog.csv'
    },
    'output_directory': './reports/',
    'schedule': {
        'frequency': 'daily',
        'time': '08:00'
    },
    'email': {
        'enabled': False,
        'recipients': ['manager@company.com'],
        'subject': 'Daily Sales Report'
    },
    'thresholds': {
        'low_sales_alert': 1000,
        'high_value_transaction': 5000
    }
}

def load_config(config_file='config.json'):
    """
    Load configuration from JSON file
    """
    import json
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    return config

def save_config(config, config_file='config.json'):
    """
    Save configuration to JSON file
    """
    import json
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=4)
    print(f"Configuration saved to {config_file}")

# Example usage
# save_config(config)

# %% [markdown]
# ## 10. Best Practices for Production Code

# %% [markdown]
# ### 1. Use Functions and Classes
# - Break code into small, reusable functions
# - Each function should do one thing well
# - Use meaningful names
#
# ### 2. Add Documentation
# ```python
# def process_data(df, threshold=100):
#     """
#     Process sales data above threshold
#     
#     Parameters:
#     - df (DataFrame): Input sales data
#     - threshold (float): Minimum sales amount
#     
#     Returns:
#     - DataFrame: Filtered and processed data
#     """
#     pass
# ```
#
# ### 3. Handle Errors
# - Use try/except blocks
# - Log errors for debugging
# - Fail gracefully
#
# ### 4. Test Your Code
# - Test with sample data
# - Handle edge cases
# - Validate outputs
#
# ### 5. Use Version Control
# - Use Git to track changes
# - Commit regularly with meaningful messages
# - Create branches for new features
#
# ### 6. Keep Secrets Safe
# - Don't hard-code passwords
# - Use environment variables
# - Use configuration files (not in Git)
#
# ### 7. Monitor and Log
# - Log important events
# - Monitor pipeline execution
# - Set up alerts for failures

# %% [markdown]
# ## Complete Example: Production-Ready Script

# %%
def main():
    """
    Main function for automated sales reporting
    """
    # Configuration
    INPUT_FILE = '../datasets/sales_data.csv'
    OUTPUT_DIR = './reports/'
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print(f"\n{'='*70}")
    print(f"SALES REPORT AUTOMATION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    try:
        # Load data
        print("[1/4] Loading data...")
        df = pd.read_csv(INPUT_FILE, parse_dates=['date'])
        print(f"      ✓ Loaded {len(df)} records")
        
        # Process data
        print("\n[2/4] Processing data...")
        df = transform_sales_data(df)
        print(f"      ✓ Processed successfully")
        
        # Generate report
        print("\n[3/4] Generating report...")
        generate_sales_report(df)
        print(f"      ✓ Report generated")
        
        # Create visualization
        print("\n[4/4] Creating visualizations...")
        dashboard_file = f'{OUTPUT_DIR}dashboard_{timestamp}.png'
        create_sales_dashboard(df, dashboard_file)
        print(f"      ✓ Dashboard saved")
        
        print(f"\n{'='*70}")
        print("AUTOMATION COMPLETED SUCCESSFULLY!")
        print(f"{'='*70}\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

# Run the main function
if __name__ == '__main__':
    # main()  # Uncomment to run
    pass

# %% [markdown]
# ## Summary
#
# In this module, you learned:
#
# ✓ **Functions**: Create reusable code blocks  
# ✓ **ETL Pipelines**: Extract, Transform, Load workflows  
# ✓ **Automated Reports**: Generate reports programmatically  
# ✓ **Visualizations**: Create dashboards for reports  
# ✓ **Scheduling**: Use Task Scheduler or cron for automation  
# ✓ **Error Handling**: Make code robust with try/except  
# ✓ **Logging**: Track pipeline execution  
# ✓ **Best Practices**: Production-ready code guidelines
#
# ### Next Steps
#
# 1. **Practice**: Convert your analyses into functions
# 2. **Experiment**: Create your own automated reports
# 3. **Schedule**: Set up a simple automated task
# 4. **Learn More**: Explore advanced topics:
#    - Plotly for interactive visualizations
#    - FastAPI for web APIs
#    - Apache Airflow for complex pipelines
#    - Docker for deployment
#
# ### Resources
#
# - **Pandas Documentation**: https://pandas.pydata.org/docs/
# - **Matplotlib Gallery**: https://matplotlib.org/stable/gallery/
# - **Python Automation**: "Automate the Boring Stuff with Python"
# - **Data Pipelines**: "Data Pipelines Pocket Reference" by James Densmore
#
# ### Congratulations! 🎉
#
# You've completed the Python Data Analysis for Beginners course!
# You now have the skills to:
# - Load and analyze data with Pandas
# - Create professional visualizations
# - Clean and transform messy data
# - Build automated data pipelines
#
# Keep practicing and happy analyzing! 📊🐍

