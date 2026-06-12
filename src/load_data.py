from sqlalchemy import create_engine, engine, text
from urllib.parse import quote_plus 
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') 

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path) 

user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')
host = os.getenv('host')
port = os.getenv('port')

def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:{port}/{database}"
    )
engine = get_engine()

def load_weather_data(table_name:str, df):
    logging.info("Loading data into table: %s", table_name)
    df.to_sql(
        name =table_name,
        con = engine,
        if_exists = 'append',
        index = False
    )
    logging.info("Data loaded successfully into table: %s", table_name)

    df_check = pd.read_sql(text(f"SELECT * FROM {table_name}"), con=engine)
    
    logging.info("Data in table %s after loading:\n%s", table_name, df_check.head())