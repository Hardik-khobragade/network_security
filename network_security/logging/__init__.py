import logging
import os
from datetime import datetime

log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)



logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info("This is a test log message.")
        print(f"Log file created at: {LOG_FILE_PATH}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"Error: {e}")