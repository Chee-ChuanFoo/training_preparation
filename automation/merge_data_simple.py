import pandas as pd

def load_data():
    df_sales = pd.read_csv("../datasets/sales_data.csv")
    df_customer = pd.read_csv("../datasets/customer_data.csv")
    df_product = pd.read_csv("../datasets/product_catalog.csv")
    return df_sales, df_customer, df_product

def merge_data(df_sales, df_customer, df_product):
    # Merge sales with customer data
    df_merged = pd.merge(df_sales, df_customer, on='customer_id', how='left')
    # Merge the result with product data
    df_merged = pd.merge(df_merged, df_product, on='product_id', how='left')
    return df_merged

def export_data(df, output_path):
    df.to_csv(output_path, index=False)

def main():
    
    # Load data
    df_sales, df_customer, df_product = load_data()
    
    # Merge data
    df_combined = merge_data(df_sales, df_customer, df_product)
    
    # Export combined data
    export_data(df_combined, '../automation/combined_data.csv')

if __name__ == '__main__':
    import sys
    sys.exit(main())