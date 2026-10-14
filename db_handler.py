# db_handler.py
import sqlite3
import pandas as pd
from datetime import datetime

class ClinicalDatabaseHandler:
    def __init__(self, workspace_name: str):
        # Sanitize filename string to avoid system path problems
        self.safe_name = "".join([c for c in workspace_name if c.isalnum() or c in ("_", "-")]).lower()
        self.db_filename = f"database_{self.safe_name}.db"
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_filename)

    def _init_db(self):
        """Initializes the active database table topology if missing."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assessment_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                player_id TEXT,
                dominant_leg TEXT,
                right_quad REAL,
                right_ham REAL,
                left_quad REAL,
                left_ham REAL,
                dom_hq REAL,
                ndom_hq REAL,
                ham_asym REAL,
                deficit_count INTEGER,
                profile_status TEXT
            )
        """)
        conn.commit()
        conn.close()

    def save_record(self, player_id: str, dominant_leg: str, r_quad: float, r_ham: float, l_quad: float, l_ham: float, analysis: dict):
        """Inserts a diagnostic record into the isolated database file."""
        conn = self._get_connection()
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        ROUNDED_dom_hq = float(f"{analysis['dom_hq']:.0f}")
        ROUNDED_ndom_hq = float(f"{analysis['ndom_hq']:.0f}")
        ROUNDED_ham_asym = float(f"{analysis['ham_asym']:.0f}")

        cursor.execute("""
            INSERT INTO assessment_results (
                timestamp, player_id, dominant_leg, right_quad, right_ham, 
                left_quad, left_ham, dom_hq, ndom_hq, ham_asym, deficit_count, profile_status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, player_id, dominant_leg, r_quad, r_ham, l_quad, l_ham, 
              ROUNDED_dom_hq, ROUNDED_ndom_hq, ROUNDED_ham_asym, 
              analysis["deficit_count"], analysis["profile_status"]))
        
        conn.commit()
        conn.close()

    def load_records(self) -> pd.DataFrame:
        """Queries the specific client data table into a DataFrame."""
        conn = self._get_connection()
        df = pd.read_sql_query("SELECT * FROM assessment_results ORDER BY id DESC", conn)
        conn.close()
        return df

    def delete_last_entry(self):
        """Removes the absolute latest record from the isolated table rows."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM assessment_results WHERE id = (SELECT MAX(id) FROM assessment_results)")
        conn.commit()
        conn.close()

    def purge_entire_database(self):
        """Completely wipes out all tracking entries inside this active database file."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM assessment_results")
        conn.commit()
        conn.close()
