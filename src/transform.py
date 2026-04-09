import pandas as pd
import uuid
import hashlib
from db_utils import get_db_engine

def generate_hash_id(text):
    """Creates a consistent 8-character ID based on text input."""
    return hashlib.md5(text.encode()).hexdigest()[:8]

def transform_and_load():
    engine = get_db_engine()

    print("🔄 Extracting raw data for transformation...")
    raw_df = pd.read_sql("SELECT * FROM raw.sales_transactions", engine)

    if raw_df.empty:
        print("⚠️ No data found in raw table.")
        return

    print("🧹 Cleaning data and generating Surrogate Keys...")
    
    # Clean Dates
    raw_df['transaction_date'] = pd.to_datetime(raw_df['transaction_date'])

    # --- THE FIX: SURROGATE KEYS ---
    # 1. Every transaction gets a random, guaranteed unique ID
    raw_df['transaction_id'] = [str(uuid.uuid4()) for _ in range(len(raw_df))]

    # 2. Hash the customer's full name to create a consistent ID 
    # (If 'Der De Ruggiero' appears twice, he gets the exact same hash ID both times!)
    raw_df['customer_id'] = (raw_df['customer_first_name'] + raw_df['customer_last_name']).apply(generate_hash_id)

    # 3. Hash the product name to create a consistent product ID
    raw_df['product_id'] = raw_df['product_name'].apply(generate_hash_id)
    # -------------------------------

    print("✂️ Splitting data into Star Schema...")
    
    # DIMENSION TABLE: Customers
    dim_customers = raw_df[[
        'customer_id', 'customer_first_name', 'customer_last_name', 'customer_country'
    ]].drop_duplicates(subset=['customer_id'])

    # DIMENSION TABLE: Products
    dim_products = raw_df[[
        'product_id', 'product_name', 'unit_price'
    ]].drop_duplicates(subset=['product_id'])

    # FACT TABLE: Sales
    fact_sales = raw_df[[
        'transaction_id', 'transaction_date', 'customer_id', 'product_id', 
        'quantity', 'sales_rep_id', 'sales_rep_name'
    ]]

    print("💾 Loading Star Schema into REFINED database layer...")
    
    dim_customers.to_sql('dim_customers', engine, schema='refined', if_exists='replace', index=False)
    dim_products.to_sql('dim_products', engine, schema='refined', if_exists='replace', index=False)
    fact_sales.to_sql('fact_sales', engine, schema='refined', if_exists='replace', index=False)

    print("✨ Transformation complete! Clean tables created in REFINED layer.")

if __name__ == "__main__":
    transform_and_load()