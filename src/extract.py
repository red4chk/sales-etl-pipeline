import os
import requests
import pandas as pd
from dotenv import load_dotenv
from db_utils import get_db_engine

# Load secrets from the config/.env file
load_dotenv(dotenv_path="../config/.env")

def extract_from_api():
    """
    Pulls data from the Mockaroo API.
    """
    api_url = os.getenv("MOCKAROO_API_URL")
    api_key = os.getenv("MOCKAROO_API_KEY")

    print("📡 Fetching data from Mockaroo API...")
    
    # Pass the API key securely in the headers, exactly like your curl command
    headers = {
        "X-API-Key": api_key
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        print("✅ Data fetched successfully!")
        # Convert the JSON response directly into a pandas DataFrame
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        print(f"❌ Failed to fetch data. Status code: {response.status_code}")
        print(response.text)
        return None

def load_to_raw(df):
    """
    Loads the DataFrame into the raw schema in PostgreSQL.
    """
    if df is None or df.empty:
        print("⚠️ No data to load.")
        return

    print(f"💾 Loading {len(df)} rows into raw.sales_transactions...")
    
    engine = get_db_engine()
    
    # Insert data into Postgres. 'append' means it adds to existing data if run multiple times.
    df.to_sql(
        name='sales_transactions',
        schema='raw',
        con=engine,
        if_exists='append',
        index=False 
    )
    print("🚀 Data loaded into RAW successfully!")

if __name__ == "__main__":
    # This block runs when you execute the script directly
    raw_data_df = extract_from_api()
    load_to_raw(raw_data_df)