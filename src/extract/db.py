"""
    Shared database connection.
"""
from sqlalchemy import create_engine

DB_URL = "postgresql+psycopg2://dwuser:devpass@localhost:5432/healthcare"

def get_engine():
    return create_engine(DB_URL)
    
   
