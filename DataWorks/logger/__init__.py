import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

log_dir = os.path.join(os.getcwd(), "log")  # Replace os.getcwd() with from_root() if needed

os.makedirs(log_dir, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,  # Log file path
    format="[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s",  # Log format
    level=logging.INFO,  # Logging level
)

logging.info("Logging setup is complete.")