# Currency Exchange ETL Pipeline & Power BI Analytics

## Project Description
This project extracts currency exchange rates from the Central Bank of Uzbekistan (CBU), 
stores them in SQL Server, transforms the data using Python and pandas, 
and visualizes it in Power BI.

## Technologies Used
- Python 3.14
- requests
- pandas
- pyodbc
- Microsoft SQL Server
- Power BI Desktop
- Windows Task Scheduler

## Pipeline Steps
1. Extract data from CBU JSON API
2. Load raw data to SQL Server (raw_currency_rates)
3. Transform data using pandas
4. Load clean data to SQL Server (clean_currency_rates)
5. Visualize in Power BI
6. Automate with Windows Task Scheduler

## How to Run
1. Install requirements: pip install -r requirements.txt
2. Configure config.py with your SQL Server details
3. Run pipeline: python run_pipeline.py
4. Pipeline runs automatically every day at 09:00 AM

## Project Structure
currency_exchange_project/
├── config.py
├── extract_to_raw.py
├── transform_to_clean.py
├── run_pipeline.py
├── run_pipeline.bat
├── requirements.txt
├── README.md
├── sql/
│   ├── create_raw_table.sql
│   └── create_clean_table.sql
└── logs/
    └── etl_log.txt
