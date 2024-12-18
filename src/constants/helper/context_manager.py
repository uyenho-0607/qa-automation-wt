import time
import logging
from contextlib import contextmanager


# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@contextmanager
def log_time(action_name):
    start_time = time.time()
    yield
    end_time = time.time()
    logging.info(f"{action_name} took {end_time - start_time:.2f} seconds")
