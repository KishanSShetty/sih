import sqlite3
db_path = 'sql_app.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
columns = [
    ('sender', 'VARCHAR', "'unknown'"),
    ('subject', 'VARCHAR', "'unknown'"),
    ('spf_status', 'VARCHAR', "'UNKNOWN'"),
    ('dkim_status', 'VARCHAR', "'UNKNOWN'"),
    ('dmarc_status', 'VARCHAR', "'UNKNOWN'"),
    ('origin_ip', 'VARCHAR', "'unknown'"),
    ('received_chain', 'VARCHAR', "'[]'"),
    ('auth_results', 'VARCHAR', "'UNKNOWN'")
]
for col_name, col_type, default_val in columns:
    try:
        cursor.execute(f"ALTER TABLE scan_results ADD COLUMN {col_name} {col_type} DEFAULT {default_val}")
    except Exception as e:
        pass
conn.commit()
conn.close()
