from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())

import os 

def init_database(user, password, database) -> SQLDatabase:
    db_uri = f"mssql+pyodbc://{user}:{password}@MKSAM22\\MSSQLSERVER01/{database}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
    return SQLDatabase.from_uri(db_uri)

def get_schema_text():
    db = init_database(
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_NAME"),
    )
    schema = db.get_table_info()
    return schema

# Example usage
print(get_schema_text())
