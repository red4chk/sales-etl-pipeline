from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

# We need to tell Airflow exactly where your 'src' folder is
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(PROJECT_ROOT, 'src')

# Default settings for our pipeline
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 8), # Start date
    'retries': 1,                       # If it fails, try again 1 time
    'retry_delay': timedelta(minutes=1),# Wait 1 minute before retrying
}

# Define the DAG
with DAG(
    'sales_daily_etl_pipeline',
    default_args=default_args,
    description='Automated Extract, Transform, Load pipeline for Sales',
    schedule_interval=timedelta(days=1), # Run this once every day!
    catchup=False
) as dag:

    # TASK 1: The 'E' in ETL
    extract_task = BashOperator(
        task_id='extract_raw_data',
        bash_command=f'cd "{SRC_DIR}" && python extract.py'
    )

    # TASK 2: The 'T' in ETL
    transform_task = BashOperator(
        task_id='transform_and_clean_data',
        bash_command=f'cd "{SRC_DIR}" && python transform.py'
    )

    # TASK 3: The 'L' in ETL (Loading the final reports)
    report_task = BashOperator(
        task_id='generate_business_reports',
        bash_command=f'cd "{SRC_DIR}" && python report.py'
    )

    # THE MAGIC: Setting the order of execution!
    # This tells Airflow: Extract -> Transform -> Report
    extract_task >> transform_task >> report_task