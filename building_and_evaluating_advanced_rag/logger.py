import logging
import os
import inspect

# Configure the logging
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s - %(levelname)s] : %(message)s')

# Create a logger object
log = logging.getLogger(__name__)



def log_info(message, filename=None):
    if filename is None:
        # Get the file name of the caller function
        filename = inspect.getframeinfo(inspect.stack()[1][0]).filename

    log.info(f'{os.path.basename(filename)} - {message}')