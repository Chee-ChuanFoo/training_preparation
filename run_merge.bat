@echo off
REM Automation script to merge customer and product data with sales data
REM This batch file activates the virtual environment and runs merge_data.py

echo ========================================
echo Data Merging Automation
echo ========================================
echo.

cd "C:\Users\Acer\OneDrive\Freelance\Dreamcatcher\01 Conducted Training\20251020 Sandisk Shanghai python for data analysis beginner\training_preparation"

REM Step 1: Activate virtual environment
echo [1/3] Activating virtual environment...
call .venv\Scripts\activate.bat

REM Step 2: Change to automation folder
echo [2/3] Navigating to automation folder...
cd automation

REM Step 3: Run the merge script
echo [3/3] Running merge_data.py...
echo.
python merge_data.py

REM Check if script ran successfully
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo SUCCESS! Data merge completed.
    echo ========================================
) else (
    echo.
    echo ========================================
    echo ERROR! Script failed with error code %ERRORLEVEL%
    echo ========================================
)

echo.
echo Press any key to exit...
pause >nul
