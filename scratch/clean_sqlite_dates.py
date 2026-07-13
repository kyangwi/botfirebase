import sqlite3

def inspect_and_clean():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    for table in tables:
        print(f"\nTable: {table}")
        # Get column info
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        
        for col in columns:
            col_id, col_name, col_type, notnull, dflt_value, pk = col
            print(f" - Column: {col_name} ({col_type})")
            
            # If the column type is DATE or DATETIME, or contains 'date' in the name
            if 'date' in col_name.lower() or col_type.upper() in ['DATE', 'DATETIME']:
                # Let's inspect a few values
                cursor.execute(f"SELECT {col_name} FROM {table} WHERE {col_name} IS NOT NULL LIMIT 5;")
                samples = [row[0] for row in cursor.fetchall()]
                print(f"   Samples: {samples}")
                
                # Check if any contain space (indicating date + time component)
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col_name} LIKE '% %';")
                count = cursor.fetchone()[0]
                if count > 0:
                    print(f"   --> Found {count} records with datetime format. Cleaning to date (YYYY-MM-DD)...")
                    # Update table to keep only the date portion (first 10 characters)
                    cursor.execute(f"UPDATE {table} SET {col_name} = SUBSTR({col_name}, 1, 10) WHERE {col_name} LIKE '% %';")
                    conn.commit()
                    print(f"   --> Cleaned successfully.")
                    
    conn.close()

if __name__ == "__main__":
    inspect_and_clean()
