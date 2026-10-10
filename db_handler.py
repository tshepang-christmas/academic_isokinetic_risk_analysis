import sqlite3

conn = sqlite3.connect("air_data.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id TEXT NOT NULL,
        test_date TEXT NOT NULL,
        right_quad REAL NOT NULL,
        right_ham REAL NOT NULL,
        left_quad REAL NOT NULL,
        left_ham REAL NOT NULL,
        hq_ratio REAL,
        asymmetry REAL,
        risk_tier TEXT
    )
""")

conn.commit()
conn.close()

print("Database and table created successfully.")