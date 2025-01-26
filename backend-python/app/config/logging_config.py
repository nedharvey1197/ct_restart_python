import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path

class ColorFormatter(logging.Formatter):
    """Custom formatter adding colors to levelname"""
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey + '%(asctime)s - %(name)s - %(levelname)s - %(message)s' + reset,
        logging.INFO: blue + '%(asctime)s - %(levelname)s - %(message)s' + reset,
        logging.WARNING: yellow + '%(asctime)s - %(levelname)s - %(message)s' + reset,
        logging.ERROR: red + '%(asctime)s - %(levelname)s - %(message)s' + reset,
        logging.CRITICAL: bold_red + '%(asctime)s - %(levelname)s - %(message)s' + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

def setup_logging():
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColorFormatter())
    root_logger.addHandler(console_handler)

    # File handler
    file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    root_logger.addHandler(file_handler)

    # Create and return application logger
    logger = logging.getLogger("clinical_trials")
    logger.info("Logging setup complete")
    return logger 