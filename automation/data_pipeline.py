"""
ETL Data Pipeline

This script demonstrates a complete Extract-Transform-Load pipeline.
It can be used as a template for your own data pipelines.

Usage:
    python data_pipeline.py
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import logging


# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pipeline.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# Configuration
CONFIG = {
    'input_files': {
        'sales': '../datasets/sales_data.csv',
        'customers': '../datasets/customer_data.csv',
        'products': '../datasets/product_catalog.csv'
    },
    'output_dir': './pipeline_output/',
    'data_quality_checks': True
}


def extract_data(filepath, **kwargs):
    """
    Extract data from source file
    
    Args:
        filepath: Path to data file
        **kwargs: Additional arguments for pd.read_csv
    
    Returns:
        DataFrame: Extracted data
    """
    logger.info(f"Extracting data from: {filepath}")
    
    try:
        df = pd.read_csv(filepath, **kwargs)
        logger.info(f"Successfully extracted {len(df)} records")
        return df
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error extracting data: {str(e)}")
        raise


def transform_sales_data(df):
    """
    Transform sales data
    
    Args:
        df: Raw sales DataFrame
    
    Returns:
        DataFrame: Transformed data
    """
    logger.info("Transforming sales data...")
    
    df_transformed = df.copy()
    
    # Convert date
    df_transformed['date'] = pd.to_datetime(df_transformed['date'])
    
    # Add time features
    df_transformed['year'] = df_transformed['date'].dt.year
    df_transformed['month'] = df_transformed['date'].dt.month
    df_transformed['quarter'] = df_transformed['date'].dt.quarter
    df_transformed['day_of_week'] = df_transformed['date'].dt.day_name()
    df_transformed['is_weekend'] = df_transformed['date'].dt.dayofweek >= 5
    
    # Categorize sales
    bins = [0, 500, 1000, float('inf')]
    labels = ['Low', 'Medium', 'High']
    df_transformed['sale_category'] = pd.cut(
        df_transformed['total_amount'], 
        bins=bins, 
        labels=labels
    )
    
    # Calculate metrics
    df_transformed['commission'] = df_transformed['total_amount'] * 0.05
    df_transformed['profit_estimate'] = df_transformed['total_amount'] * 0.25
    
    # Standardize text fields
    df_transformed['region'] = df_transformed['region'].str.upper()
    df_transformed['payment_method'] = df_transformed['payment_method'].str.title()
    
    logger.info(f"Transformation complete: {len(df_transformed)} records")
    return df_transformed


def transform_customer_data(df):
    """
    Transform customer data
    
    Args:
        df: Raw customer DataFrame
    
    Returns:
        DataFrame: Transformed data
    """
    logger.info("Transforming customer data...")
    
    df_transformed = df.copy()
    
    # Convert dates
    df_transformed['signup_date'] = pd.to_datetime(df_transformed['signup_date'])
    
    # Calculate customer tenure
    df_transformed['days_as_customer'] = (
        pd.Timestamp.now() - df_transformed['signup_date']
    ).dt.days
    
    # Create full name
    df_transformed['full_name'] = (
        df_transformed['first_name'] + ' ' + df_transformed['last_name']
    )
    
    # Standardize
    df_transformed['state'] = df_transformed['state'].str.upper()
    df_transformed['email'] = df_transformed['email'].str.lower()
    
    # Calculate value per purchase
    df_transformed['avg_purchase_value'] = (
        df_transformed['lifetime_value'] / df_transformed['total_purchases']
    ).round(2)
    
    logger.info(f"Transformation complete: {len(df_transformed)} records")
    return df_transformed


def validate_data(df, checks):
    """
    Perform data quality checks
    
    Args:
        df: DataFrame to validate
        checks: Dictionary of validation rules
    
    Returns:
        bool: True if all checks pass
    """
    logger.info("Performing data quality checks...")
    
    all_passed = True
    
    # Check for required columns
    if 'required_columns' in checks:
        missing_cols = set(checks['required_columns']) - set(df.columns)
        if missing_cols:
            logger.error(f"Missing required columns: {missing_cols}")
            all_passed = False
        else:
            logger.info("✓ All required columns present")
    
    # Check for null values
    if 'no_nulls' in checks:
        null_cols = df[checks['no_nulls']].isnull().sum()
        null_cols = null_cols[null_cols > 0]
        if not null_cols.empty:
            logger.warning(f"Null values found: {null_cols.to_dict()}")
        else:
            logger.info("✓ No null values in critical columns")
    
    # Check data types
    if 'data_types' in checks:
        for col, expected_type in checks['data_types'].items():
            if df[col].dtype != expected_type:
                logger.warning(f"Column '{col}' has type {df[col].dtype}, expected {expected_type}")
    
    # Check value ranges
    if 'value_ranges' in checks:
        for col, (min_val, max_val) in checks['value_ranges'].items():
            out_of_range = df[(df[col] < min_val) | (df[col] > max_val)]
            if not out_of_range.empty:
                logger.warning(f"Column '{col}' has {len(out_of_range)} values outside range [{min_val}, {max_val}]")
    
    if all_passed:
        logger.info("✓ All data quality checks passed")
    
    return all_passed


def load_data(df, output_path, format='csv'):
    """
    Load data to destination
    
    Args:
        df: DataFrame to save
        output_path: Destination path
        format: Output format ('csv' or 'excel')
    
    Returns:
        bool: True if successful
    """
    logger.info(f"Loading data to: {output_path}")
    
    try:
        if format == 'csv':
            df.to_csv(output_path, index=False)
        elif format == 'excel':
            df.to_excel(output_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Successfully loaded {len(df)} records")
        return True
    except Exception as e:
        logger.error(f"Error loading data: {str(e)}")
        raise


def run_pipeline():
    """
    Execute the complete ETL pipeline
    """
    logger.info("="*70)
    logger.info("STARTING ETL PIPELINE")
    logger.info("="*70)
    
    # Create output directory
    os.makedirs(CONFIG['output_dir'], exist_ok=True)
    
    try:
        # ==================== EXTRACT ====================
        logger.info("\n[EXTRACT PHASE]")
        
        df_sales_raw = extract_data(
            CONFIG['input_files']['sales'],
            parse_dates=['date']
        )
        
        df_customers_raw = extract_data(
            CONFIG['input_files']['customers'],
            parse_dates=['signup_date']
        )
        
        df_products_raw = extract_data(
            CONFIG['input_files']['products']
        )
        
        # ==================== TRANSFORM ====================
        logger.info("\n[TRANSFORM PHASE]")
        
        df_sales = transform_sales_data(df_sales_raw)
        df_customers = transform_customer_data(df_customers_raw)
        
        # Merge datasets for enriched sales data
        logger.info("Merging datasets...")
        df_enriched = pd.merge(
            df_sales,
            df_customers[['customer_id', 'full_name', 'customer_segment', 'city', 'state']],
            on='customer_id',
            how='left'
        )
        
        df_enriched = pd.merge(
            df_enriched,
            df_products[['product_id', 'product_name', 'category', 'subcategory']],
            on='product_id',
            how='left'
        )
        
        logger.info(f"Merged dataset: {len(df_enriched)} records")
        
        # ==================== VALIDATE ====================
        if CONFIG['data_quality_checks']:
            logger.info("\n[VALIDATION PHASE]")
            
            sales_checks = {
                'required_columns': ['transaction_id', 'date', 'total_amount'],
                'no_nulls': ['transaction_id', 'date', 'total_amount'],
                'value_ranges': {'total_amount': (0, 100000)}
            }
            
            validate_data(df_enriched, sales_checks)
        
        # ==================== LOAD ====================
        logger.info("\n[LOAD PHASE]")
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save transformed datasets
        load_data(
            df_sales,
            os.path.join(CONFIG['output_dir'], f'sales_transformed_{timestamp}.csv')
        )
        
        load_data(
            df_customers,
            os.path.join(CONFIG['output_dir'], f'customers_transformed_{timestamp}.csv')
        )
        
        load_data(
            df_enriched,
            os.path.join(CONFIG['output_dir'], f'sales_enriched_{timestamp}.csv')
        )
        
        # Create summary statistics
        logger.info("\nGenerating summary statistics...")
        summary = {
            'pipeline_run_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_sales': float(df_sales['total_amount'].sum()),
            'total_transactions': len(df_sales),
            'unique_customers': int(df_sales['customer_id'].nunique()),
            'unique_products': int(df_sales['product_id'].nunique()),
            'date_range': f"{df_sales['date'].min()} to {df_sales['date'].max()}"
        }
        
        summary_df = pd.DataFrame([summary])
        load_data(
            summary_df,
            os.path.join(CONFIG['output_dir'], f'pipeline_summary_{timestamp}.csv')
        )
        
        logger.info("\n" + "="*70)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("="*70)
        
        return True
        
    except Exception as e:
        logger.error(f"\nPIPELINE FAILED: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def main():
    """Main entry point"""
    success = run_pipeline()
    return 0 if success else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())

