"""
Automated Sales Report Generator

This script generates a comprehensive sales report including:
- Text-based statistical report
- Visual dashboard
- Processed data export

Usage:
    python report_generator.py
    
Or scheduled via Task Scheduler (Windows) or cron (Mac/Linux)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import sys

# Configuration
DATA_DIR = '../datasets/'
OUTPUT_DIR = './reports/'
SALES_FILE = 'sales_data.csv'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_and_transform_data(filepath):
    """Load and transform sales data"""
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath, parse_dates=['date'])
    
    # Add derived columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    df['day_of_week'] = df['date'].dt.day_name()
    
    # Categorize sales
    def categorize_sale(amount):
        if amount >= 1000:
            return 'High'
        elif amount >= 500:
            return 'Medium'
        else:
            return 'Low'
    
    df['sale_category'] = df['total_amount'].apply(categorize_sale)
    
    print(f"Loaded and transformed {len(df)} records")
    return df


def generate_text_report(df, output_file):
    """Generate text-based sales report"""
    report_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(output_file, 'w') as f:
        f.write("=" * 70 + "\n")
        f.write(f"SALES REPORT - Generated on {report_date}\n")
        f.write("=" * 70 + "\n\n")
        
        # Overall metrics
        f.write("OVERALL METRICS\n")
        f.write("-" * 70 + "\n")
        f.write(f"Total Revenue:        ${df['total_amount'].sum():>15,.2f}\n")
        f.write(f"Average Transaction:  ${df['total_amount'].mean():>15,.2f}\n")
        f.write(f"Total Transactions:   {len(df):>18,}\n")
        f.write(f"Unique Customers:     {df['customer_id'].nunique():>18,}\n")
        f.write(f"Unique Products:      {df['product_id'].nunique():>18,}\n\n")
        
        # Regional breakdown
        f.write("REGIONAL BREAKDOWN\n")
        f.write("-" * 70 + "\n")
        regional_sales = df.groupby('region')['total_amount'].agg(['sum', 'mean', 'count'])
        regional_sales.columns = ['Total_Revenue', 'Avg_Transaction', 'Num_Transactions']
        regional_sales = regional_sales.sort_values('Total_Revenue', ascending=False)
        
        for region, row in regional_sales.iterrows():
            f.write(f"\n{region}:\n")
            f.write(f"  Total Revenue:     ${row['Total_Revenue']:,.2f}\n")
            f.write(f"  Avg Transaction:   ${row['Avg_Transaction']:,.2f}\n")
            f.write(f"  Transactions:      {int(row['Num_Transactions']):,}\n")
        
        # Top performers
        f.write("\n\nTOP PERFORMERS\n")
        f.write("-" * 70 + "\n")
        
        top_products = df.groupby('product_id')['total_amount'].sum().nlargest(5)
        f.write("\nTop 5 Products by Revenue:\n")
        for i, (product, revenue) in enumerate(top_products.items(), 1):
            f.write(f"  {i}. {product}: ${revenue:,.2f}\n")
        
        top_reps = df.groupby('sales_rep')['total_amount'].sum().nlargest(5)
        f.write("\nTop 5 Sales Representatives:\n")
        for i, (rep, revenue) in enumerate(top_reps.items(), 1):
            f.write(f"  {i}. {rep}: ${revenue:,.2f}\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 70 + "\n")
    
    print(f"Text report saved to: {output_file}")


def generate_dashboard(df, output_file):
    """Generate visual dashboard"""
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Plot 1: Revenue by Region
    ax1 = fig.add_subplot(gs[0, :2])
    region_sales = df.groupby('region')['total_amount'].sum().sort_values(ascending=False)
    ax1.bar(region_sales.index, region_sales.values, color='#2E86AB')
    ax1.set_title('Total Revenue by Region', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Revenue ($)')
    ax1.grid(axis='y', alpha=0.3)
    
    # Plot 2: Key Metrics
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
    
    # Plot 3: Payment Methods
    ax3 = fig.add_subplot(gs[1, 0])
    payment_counts = df['payment_method'].value_counts()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    ax3.pie(payment_counts.values, labels=payment_counts.index, autopct='%1.0f%%',
            colors=colors, textprops={'fontsize': 9})
    ax3.set_title('Payment Methods', fontsize=12, fontweight='bold')
    
    # Plot 4: Daily Sales Trend
    ax4 = fig.add_subplot(gs[1, 1:])
    daily_sales = df.groupby('date')['total_amount'].sum().sort_index()
    ax4.plot(daily_sales.index, daily_sales.values, linewidth=2, color='#2ECC71')
    ax4.set_title('Daily Sales Trend', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Sales ($)')
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(True, alpha=0.3)
    
    # Plot 5: Top Products
    ax5 = fig.add_subplot(gs[2, :2])
    top_products = df.groupby('product_id')['total_amount'].sum().nlargest(10)
    ax5.barh(range(len(top_products)), top_products.values, color='coral')
    ax5.set_yticks(range(len(top_products)))
    ax5.set_yticklabels(top_products.index)
    ax5.set_xlabel('Revenue ($)')
    ax5.set_title('Top 10 Products by Revenue', fontsize=12, fontweight='bold')
    ax5.grid(axis='x', alpha=0.3)
    
    # Plot 6: Sales Distribution
    ax6 = fig.add_subplot(gs[2, 2])
    ax6.hist(df['total_amount'], bins=30, color='#9B59B6', edgecolor='black', alpha=0.7)
    ax6.axvline(df['total_amount'].mean(), color='red', linestyle='--', linewidth=2)
    ax6.set_xlabel('Amount ($)')
    ax6.set_ylabel('Frequency')
    ax6.set_title('Transaction Distribution', fontsize=12, fontweight='bold')
    
    plt.suptitle(f'SALES DASHBOARD - {datetime.now().strftime("%Y-%m-%d")}',
                 fontsize=18, fontweight='bold', y=0.98)
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Dashboard saved to: {output_file}")


def main():
    """Main function"""
    print("\n" + "="*70)
    print(f"AUTOMATED SALES REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70 + "\n")
    
    try:
        # Generate timestamp for filenames
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Load data
        print("[1/4] Loading and processing data...")
        df = load_and_transform_data(os.path.join(DATA_DIR, SALES_FILE))
        
        # Generate text report
        print("\n[2/4] Generating text report...")
        text_report = os.path.join(OUTPUT_DIR, f'sales_report_{timestamp}.txt')
        generate_text_report(df, text_report)
        
        # Generate dashboard
        print("\n[3/4] Creating visual dashboard...")
        dashboard_file = os.path.join(OUTPUT_DIR, f'sales_dashboard_{timestamp}.png')
        generate_dashboard(df, dashboard_file)
        
        # Export processed data
        print("\n[4/4] Exporting processed data...")
        data_export = os.path.join(OUTPUT_DIR, f'sales_processed_{timestamp}.csv')
        df.to_csv(data_export, index=False)
        print(f"Data exported to: {data_export}")
        
        print("\n" + "="*70)
        print("REPORT GENERATION COMPLETED SUCCESSFULLY!")
        print("="*70)
        print(f"\nGenerated files:")
        print(f"  1. {text_report}")
        print(f"  2. {dashboard_file}")
        print(f"  3. {data_export}")
        print("")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

