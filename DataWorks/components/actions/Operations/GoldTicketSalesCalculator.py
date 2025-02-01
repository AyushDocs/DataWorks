import sqlite3
from dataclasses import dataclass
from DataWorks.logger import logging


@dataclass
class GoldTicketSalesCalculator:
    database_file:str
    table:str
    output_file:str
    def calculate(self):

        with sqlite3.connect(self.database_file) as conn:
            cursor = conn.cursor()
            query = f"SELECT SUM(units * price) FROM {self.table} WHERE type = 'Gold'"
            logging.info(f"Executing query: {query}")
            cursor.execute(query)
            total_sales = cursor.fetchone()[0] or 0

            with open(self.output_file, "w") as f:
                f.write(str(total_sales))

            logging.info(f"Successfully calculated gold ticket sales: {total_sales}")
            conn.close()