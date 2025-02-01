from DataWorks.logger import logging
import subprocess
from dataclasses import dataclass

@dataclass
class MarkdownFormatter:
    input_file:str
    prettier_version:str


    def format(self):
        logging.info(f"Formatting markdown file {self.input_file} with formatter prettier@{self.prettier_version}")
        subprocess.run(f" npx prettier@{self.prettier_version} --write {self.input_file}", shell=True, check=True)
        logging.info(f"Successfully formatted markdown file {self.input_file} with formatter prettier@{self.prettier_version}")
