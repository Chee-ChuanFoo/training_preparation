"""
Setup Verification Script

Run this script to verify your Python environment is correctly configured
for the Python Data Analysis course.

Usage:
    python verify_setup.py
"""

import sys

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.7+)")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed and importable"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = __import__(import_name)
        version = getattr(module, '__version__', 'unknown')
        print(f"  ✓ {package_name} {version}")
        return True
    except ImportError:
        print(f"  ✗ {package_name} NOT INSTALLED")
        return False

def check_datasets():
    """Check if sample datasets are present"""
    import os
    
    print("\nChecking datasets...")
    datasets = [
        'sales_data.csv',
        'customer_data.csv',
        'product_catalog.csv',
        'web_traffic.csv',
        'survey_results.csv'
    ]
    
    all_present = True
    for dataset in datasets:
        path = os.path.join('datasets', dataset)
        if os.path.exists(path):
            size_mb = os.path.getsize(path) / 1024 / 1024
            print(f"  ✓ {dataset} ({size_mb:.2f} MB)")
        else:
            print(f"  ✗ {dataset} NOT FOUND")
            all_present = False
    
    return all_present

def check_jupyter():
    """Check if Jupyter is installed"""
    print("\nChecking Jupyter...")
    try:
        import jupyter
        print("  ✓ Jupyter installed")
        return True
    except ImportError:
        # Jupyter might not have __init__.py, check notebook instead
        try:
            import notebook
            print("  ✓ Jupyter Notebook installed")
            return True
        except ImportError:
            print("  ✗ Jupyter NOT INSTALLED")
            return False

def run_quick_test():
    """Run a quick data analysis test"""
    print("\nRunning quick test...")
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        
        # Create sample data
        df = pd.DataFrame({
            'A': np.random.randint(1, 100, 10),
            'B': np.random.randint(1, 100, 10)
        })
        
        # Perform operations
        total = df['A'].sum()
        avg = df['B'].mean()
        
        # Create a simple plot (don't show it)
        fig, ax = plt.subplots()
        ax.plot(df['A'], df['B'])
        plt.close(fig)
        
        print("  ✓ Basic operations work correctly")
        return True
    except Exception as e:
        print(f"  ✗ Error during test: {str(e)}")
        return False

def main():
    """Main verification function"""
    print("="*60)
    print("Python Data Analysis - Setup Verification")
    print("="*60)
    
    all_checks = []
    
    # Check Python version
    all_checks.append(check_python_version())
    
    # Check required packages
    print("\nChecking required packages...")
    required_packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('openpyxl', 'openpyxl'),
        ('xlrd', 'xlrd'),
    ]
    
    for package_name, import_name in required_packages:
        all_checks.append(check_package(package_name, import_name))
    
    # Check Jupyter
    all_checks.append(check_jupyter())
    
    # Check datasets
    all_checks.append(check_datasets())
    
    # Run quick test
    all_checks.append(run_quick_test())
    
    # Summary
    print("\n" + "="*60)
    if all(all_checks):
        print("✓ ALL CHECKS PASSED!")
        print("="*60)
        print("\nYou're ready for the course! 🎉")
        print("\nNext steps:")
        print("  1. Start Jupyter Notebook: jupyter notebook")
        print("  2. Open: notebooks/01_python_quickstart.ipynb")
        print("  3. Begin learning!")
    else:
        print("✗ SOME CHECKS FAILED")
        print("="*60)
        print("\nPlease install missing packages:")
        print("\nUsing Anaconda:")
        print("  - Anaconda includes all required packages by default")
        print("\nUsing pip:")
        print("  pip install pandas matplotlib seaborn jupyter openpyxl xlrd")
        print("\nIf datasets are missing, run:")
        print("  python generate_datasets.py")
    
    print("")
    return 0 if all(all_checks) else 1

if __name__ == '__main__':
    sys.exit(main())

