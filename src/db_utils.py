from sqlalchemy import create_engine
import os

def get_db_engine():
    db_user = "admin"
    db_password = "adminpassword"
    
    # THE FIX: Read from the environment, default to localhost
    db_host = os.getenv("DB_HOST", "localhost") 
    
    db_port = "5433" 
    db_name = "sales_db"

    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
    return engine