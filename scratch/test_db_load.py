import os
from langchain_community.utilities import SQLDatabase

def test_conn():
    base_dir = r"d:\JOSH\AgenticSQLChatBot"
    db_path = os.path.join(base_dir, "data.db")
    db_uri = f"sqlite:///{db_path}"
    
    print(f"Database path: {db_path}")
    print(f"Database URI: {db_uri}")
    print(f"File exists: {os.path.exists(db_path)}")
    
    try:
        db = SQLDatabase.from_uri(db_uri)
        print("SQLDatabase object successfully created.")
        print(f"Dialect: {db.dialect}")
        print("Available tables:")
        print(db.get_usable_table_names())
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_conn()
