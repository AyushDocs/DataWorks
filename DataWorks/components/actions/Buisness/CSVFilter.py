import logging
import pandas as pd
import io
from dataclasses import dataclass

@dataclass
class CSVFilter:
    file_content: str
    filter_column: str
    filter_value: str

    def filter(self) -> dict:
        logging.info("Filtering CSV data")

        if not self.file_content:
            return {"error": "file_content is required"}
        if not self.filter_column or not self.filter_value:
            return {"error": "filter_column and filter_value are required"}

        df = pd.read_csv(io.StringIO(self.file_content))

        if self.filter_column not in df.columns:
            return {"error": f"Column '{self.filter_column}' not found in the CSV file"}

        filtered_df = df[df[self.filter_column] == self.filter_value]
        filtered_data = filtered_df.to_dict(orient="records")

        logging.info("CSV data filtered successfully")
        return {"filtered_data": filtered_data}
