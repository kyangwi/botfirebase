import os
import sys
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, inspect
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def main():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    
    if not all([user, password, database]):
        print("Error: Missing database environment variables in .env")
        sys.exit(1)
        
    # Connection string from test_connetion.py
    mssql_uri = f"mssql+pyodbc://{user}:{password}@MKSAM22\\MSSQLSERVER01/{database}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
    sqlite_uri = "sqlite:///data.db"
    
    print(f"Connecting to source MS SQL database at: MKSAM22\\MSSQLSERVER01/{database}")
    try:
        src_engine = create_engine(mssql_uri)
        # Test connection
        with src_engine.connect() as conn:
            print("Successfully connected to MS SQL Server.")
    except Exception as e:
        print(f"Failed to connect to MS SQL Server: {e}")
        print("Falling back to localhost\\MSSQLSERVER01...")
        mssql_uri = f"mssql+pyodbc://{user}:{password}@localhost\\MSSQLSERVER01/{database}?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"
        try:
            src_engine = create_engine(mssql_uri)
            with src_engine.connect() as conn:
                print("Successfully connected to MS SQL Server at localhost.")
        except Exception as e2:
            print(f"Failed to connect to localhost MS SQL Server: {e2}")
            sys.exit(1)

    print("Connecting to target SQLite database (data.db)...")
    tgt_engine = create_engine(sqlite_uri)
    
    src_meta = MetaData()
    print("Reflecting tables from MS SQL Server...")
    src_meta.reflect(bind=src_engine)
    
    # We want to transfer tables in order of dependencies (or turn off PRAGMA foreign_keys during creation and insertion)
    print("Disabling foreign keys in target SQLite for schema creation...")
    with tgt_engine.connect() as conn:
        conn.execute(sys.modules['sqlalchemy'].text("PRAGMA foreign_keys = OFF;"))
        
    print("\nCreating tables in SQLite...")
    # Clean collation and other MSSQL-specific elements before creating in SQLite
    for table_name, table in src_meta.tables.items():
        print(f"Processing table schema: {table_name}")
        for column in table.columns:
            # SQLite does not support collations like SQL_Latin1_General_CP1_CI_AS
            if hasattr(column.type, 'collation'):
                column.type.collation = None
                
    # Create all tables
    src_meta.create_all(bind=tgt_engine)
    print("Tables created successfully.")
    
    # Copy data table by table
    print("\nMigrating data table by table...")
    inspector = inspect(src_engine)
    table_names = inspector.get_table_names()
    
    # Sort tables so dependencies are handled correctly, or insert with foreign keys disabled
    # Since SQLite lets us disable foreign keys during connection session, we will keep it disabled.
    with tgt_engine.begin() as conn:
        conn.execute(sys.modules['sqlalchemy'].text("PRAGMA foreign_keys = OFF;"))
        
        for table_name in table_names:
            print(f"Migrating table {table_name}...")
            # Delete existing data if any
            conn.execute(sys.modules['sqlalchemy'].text(f"DELETE FROM {table_name}"))
            
            # Read from source
            df = pd.read_sql_table(table_name, con=src_engine)
            print(f"  Found {len(df)} rows. Inserting into SQLite...")
            
            if not df.empty:
                # Write to SQLite using the active connection transaction
                df.to_sql(table_name, con=conn, if_exists='append', index=False)
                print(f"  Successfully inserted {len(df)} rows into SQLite table {table_name}.")
            else:
                print(f"  Table {table_name} is empty. Skipped data insertion.")
                
        # Re-enable foreign keys
        conn.execute(sys.modules['sqlalchemy'].text("PRAGMA foreign_keys = ON;"))
        print("\nForeign keys re-enabled on SQLite database.")
        
    print("\nDatabase migration completed successfully!")

if __name__ == "__main__":
    main()
