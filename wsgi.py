from DataWorks.components.app import get_app  # Import your app factory function
from DataWorks.logger import logging

app = get_app(__name__)

if __name__ == "__main__":
    logging.info("Starting app on port 5000")
    app.run(port=5007)
