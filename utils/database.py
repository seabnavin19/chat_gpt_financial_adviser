import os
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine
import pandas as pd

class Connection:
    def __init__(self):
        pass

    def create_engine(self):
        connection_url = "mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}".format(
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=3306,  # Replace with the appropriate port number
            database=os.getenv("DB_NAME"),
        )
        
        engine = create_engine(connection_url)
        return engine




