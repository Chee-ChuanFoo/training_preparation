"""
Data Merging Automation Script

This script performs left joins to combine customer and product data with sales data.
Output: combined_data.csv

Usage:
    python merge_data.py
"""

import pandas as pd
import os
from datetime import datetime
import logging


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('merge_data.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# Configuration
CONFIG = {
    'input_files': {
        'sales': 'C',
        'customers': '../datasets/customer_data.csv',
        'products': '../datasets/product_catalog.csv'
    },
    'output_file': './combined_data.csv'
}


def load_data():
    """
    Load all required data files
    
    Returns:
        tuple: (sales_df, customers_df, products_df)
    """
    logger.info("Loading data files...")
    
    try:
        # Load sales data
        logger.info(f"Loading sales data from: {CONFIG['input_files']['sales']}")
        df_sales = pd.read_csv(CONFIG['input_files']['sales'])
        logger.info(f"  ✓ Loaded {len(df_sales):,} sales records")
        
        # Load customer data
        logger.info(f"Loading customer data from: {CONFIG['input_files']['customers']}")
        df_customers = pd.read_csv(CONFIG['input_files']['customers'])
        logger.info(f"  ✓ Loaded {len(df_customers):,} customer records")
        
        # Load product data
        logger.info(f"Loading product data from: {CONFIG['input_files']['products']}")
        df_products = pd.read_csv(CONFIG['input_files']['products'])
        logger.info(f"  ✓ Loaded {len(df_products):,} product records")
        
        return df_sales, df_customers, df_products
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        raise


def merge_data(df_sales, df_customers, df_products):
    """
    Perform left joins to combine all data
    
    Args:
        df_sales: Sales DataFrame
        df_customers: Customer DataFrame
        df_products: Product DataFrame
    
    Returns:
        DataFrame: Combined data
    """
    logger.info("\nMerging data...")
    
    # Step 1: Left join sales with customer data
    logger.info("Step 1: Left joining sales data with customer data on 'customer_id'...")
    df_combined = pd.merge(
        df_sales,
        df_customers,
        on='customer_id',
        how='left',
        suffixes=('', '_customer')
    )
    logger.info(f"  ✓ After customer merge: {len(df_combined):,} records")
    
    # Check for unmatched customers
    unmatched_customers = df_combined['first_name'].isnull().sum()
    if unmatched_customers > 0:
        logger.warning(f"  ⚠ {unmatched_customers} sales records without matching customer data")
    
    # Step 2: Left join with product data
    logger.info("Step 2: Left joining combined data with product data on 'product_id'...")
    df_combined = pd.merge(
        df_combined,
        df_products,
        on='product_id',
        how='left',
        suffixes=('', '_product')
    )
    logger.info(f"  ✓ After product merge: {len(df_combined):,} records")
    
    # Check for unmatched products
    unmatched_products = df_combined['product_name'].isnull().sum()
    if unmatched_products > 0:
        logger.warning(f"  ⚠ {unmatched_products} sales records without matching product data")
    
    return df_combined


def generate_summary(df_combined):
    """
    Generate summary statistics about the combined data
    
    Args:
        df_combined: Combined DataFrame
    
    Returns:
        dict: Summary statistics
    """
    logger.info("\nGenerating summary statistics...")
    
    summary = {
        'Total Records': len(df_combined),
        'Unique Transactions': df_combined['transaction_id'].nunique(),
        'Unique Customers': df_combined['customer_id'].nunique(),
        'Unique Products': df_combined['product_id'].nunique(),
        'Total Columns': len(df_combined.columns),
        'Date Range': f"{df_combined['date'].min()} to {df_combined['date'].max()}",
        'Total Sales Amount': f"${df_combined['total_amount'].sum():,.2f}",
        'Average Transaction': f"${df_combined['total_amount'].mean():,.2f}",
        'Missing Customer Info': df_combined['first_name'].isnull().sum(),
        'Missing Product Info': df_combined['product_name'].isnull().sum(),
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    logger.info("\n" + "="*70)
    logger.info("SUMMARY STATISTICS")
    logger.info("="*70)
    for key, value in summary.items():
        logger.info(f"{key:.<30} {value}")
    logger.info("="*70)
    
    return summary


def save_combined_data(df_combined, output_path):
    """
    Save combined data to CSV file
    
    Args:
        df_combined: Combined DataFrame
        output_path: Output file path
    
    Returns:
        bool: True if successful
    """
    logger.info(f"\nSaving combined data to: {output_path}")
    
    try:
        df_combined.to_csv(output_path, index=False)
        logger.info(f"  ✓ Successfully saved {len(df_combined):,} records")
        logger.info(f"  ✓ File size: {os.path.getsize(output_path) / 1024:.2f} KB")
        return True
        
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise


def display_column_info(df_combined):
    """
    Display information about the combined dataset columns
    
    Args:
        df_combined: Combined DataFrame
    """
    logger.info("\n" + "="*70)
    logger.info("COLUMN INFORMATION")
    logger.info("="*70)
    logger.info(f"Total columns: {len(df_combined.columns)}\n")
    
    # Group columns by source
    sales_cols = ['transaction_id', 'date', 'product_id', 'customer_id', 'quantity', 
                  'unit_price', 'region', 'sales_rep', 'payment_method', 'total_amount']
    customer_cols = ['first_name', 'last_name', 'email', 'phone', 'city', 'state', 
                     'signup_date', 'customer_segment', 'total_purchases', 'lifetime_value']
    product_cols = ['product_name', 'category', 'subcategory', 'cost_price', 'retail_price', 
                    'stock_quantity', 'supplier', 'weight_kg', 'is_active', 'profit_margin']
    
    logger.info("From Sales Data:")
    for col in sales_cols:
        if col in df_combined.columns:
            logger.info(f"  - {col}")
    
    logger.info("\nFrom Customer Data:")
    for col in customer_cols:
        if col in df_combined.columns:
            logger.info(f"  - {col}")
    
    logger.info("\nFrom Product Data:")
    for col in product_cols:
        if col in df_combined.columns:
            logger.info(f"  - {col}")
    
    logger.info("="*70)


def main():
    """
    Main execution function
    """
    logger.info("="*70)
    logger.info("DATA MERGING AUTOMATION SCRIPT")
    logger.info("="*70)
    
    try:
        # Step 1: Load data
        df_sales, df_customers, df_products = load_data()
        
        # Step 2: Merge data (left joins)
        df_combined = merge_data(df_sales, df_customers, df_products)
        
        # Step 3: Display column information
        display_column_info(df_combined)
        
        # Step 4: Generate summary
        summary = generate_summary(df_combined)
        
        # Step 5: Save combined data
        save_combined_data(df_combined, CONFIG['output_file'])
        
        logger.info("\n" + "="*70)
        logger.info("✓ DATA MERGING COMPLETED SUCCESSFULLY!")
        logger.info("="*70)
        logger.info(f"\nOutput file: {os.path.abspath(CONFIG['output_file'])}")
        
        return 0
        
    except Exception as e:
        logger.error(f"\n✗ DATA MERGING FAILED: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
