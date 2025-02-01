import sqlite3
import duckdb
import pandas as pd
from dataclasses import dataclass
from DataWorks.logger import logging

@dataclass
class SQLQueryRunner:
    db_type: str
    db_connection: str
    query: str

    def run(self) -> pd.DataFrame:
        logging.info(f"Running SQL query on {self.db_type} database")

        if self.db_type == "sqlite":
            conn = sqlite3.connect(self.db_connection)
        elif self.db_type == "duckdb":
            conn = duckdb.connect(self.db_connection)
        else:
            raise ValueError("Unsupported database type. Use 'sqlite' or 'duckdb'.")

        pd.read_sql_query(self.query, conn)
        conn.close()

        logging.info("SQL query executed successfully")
