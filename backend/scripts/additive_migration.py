import sqlite3
import os

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql_app.db')

print(f"Connecting to database at {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

columns_to_add = [
    ("trust_score", "FLOAT", "0.0"),
    ("category", "VARCHAR", "'UNKNOWN'"),
    ("auth_results", "VARCHAR", "'UNKNOWN'")
]

for col_name, col_type, default_val in columns_to_add:
    try:
        cursor.execute(f"ALTER TABLE scan_results ADD COLUMN {col_name} {col_type} DEFAULT {default_val}")
        print(f"Added column {col_name}")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print(f"Column {col_name} already exists.")
        else:
            print(f"Error adding {col_name}: {e}")

conn.commit()
conn.close()
print("Migration completed.")
