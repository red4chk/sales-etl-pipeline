import pandas as pd
from db_utils import get_db_engine

def generate_reports():
    """
    Reads from the refined Star Schema, calculates revenue, 
    and generates aggregated business reports.
    """
    engine = get_db_engine()
    print("📊 Fetching clean data from the Star Schema...")

    # Here we write a SQL query to join our fact and dimension tables together
    # We also calculate the total_revenue right in the query!
    query = """
        SELECT 
            f.transaction_id,
            c.customer_country,
            p.product_name,
            f.quantity,
            p.unit_price,
            (f.quantity * p.unit_price) AS total_revenue
        FROM refined.fact_sales f
        JOIN refined.dim_customers c ON f.customer_id = c.customer_id
        JOIN refined.dim_products p ON f.product_id = p.product_id
    """
    
    # Load the joined data into a Pandas DataFrame
    df = pd.read_sql(query, engine)

    if df.empty:
        print("⚠️ No data available to generate reports.")
        return

    print("📈 Aggregating business metrics...")
    
    # REPORT 1: Total Revenue by Country
    # Group by country, sum the revenue, and sort from highest to lowest
    country_report = df.groupby('customer_country')['total_revenue'].sum().reset_index()
    country_report = country_report.sort_values(by='total_revenue', ascending=False)

    # REPORT 2: Total Revenue by Product
    # Group by product, sum the revenue, and sort from highest to lowest
    product_report = df.groupby('product_name')['total_revenue'].sum().reset_index()
    product_report = product_report.sort_values(by='total_revenue', ascending=False)

    print("💾 Saving reports to the REPORT database layer...")
    
    # Load these final, polished tables into the 'report' schema
    country_report.to_sql('sales_by_country', engine, schema='report', if_exists='replace', index=False)
    product_report.to_sql('sales_by_product', engine, schema='report', if_exists='replace', index=False)

    print("✅ Reports successfully generated and saved! The ETL logic is complete.")

if __name__ == "__main__":
    generate_reports()