from DataWorks.logger import logging
from dataclasses import dataclass
import subprocess


@dataclass
class PythonScriptRunner:
    python_script_url: str

    def execute(self):
        if not self.python_script_url.endswith(".py"):
            logging.error("Invalid script URL: Not a Python file")
            return
        logging.info(f"Running script {self.python_script_url}")
        logging.warning(
            f"Running script {self.python_script_url} which may potentially harm the system"
        )
        subprocess.run(
            f"uv run {self.python_script_url} 24f2004275@ds.study.iitm.ac.in",
            shell=True,
            check=True,
        )
        logging.info(f"Ran script {self.python_script_url}")
