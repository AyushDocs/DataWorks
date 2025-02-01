from dataclasses import dataclass
import os
from DataWorks.logger import logging


@dataclass
class RecentLogsWriter:
    input_directory:str
    output_file:str
    limit:str    
    def write(self):
        log_files = [f for f in os.listdir(self.input_directory) if f.endswith(".log")]
        log_files.sort(
            key=lambda f: os.path.getmtime(os.path.join(self.input_directory, f)), reverse=True
        )
        with open(self.output_file, "w") as out_f:
            for log_file in log_files[:self.limit]:
                with open(os.path.join(self.input_directory, log_file), "r") as f:
                    first_line = f.readline().strip()
                    out_f.write(first_line + "\n")
        logging.info("Extracted recent logs successfully")