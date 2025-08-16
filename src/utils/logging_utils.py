import logging

from colorama import Fore, Style

from src.data.project_info import StepLogs

def record_steps_log(func):
    def wrapper(*args, **kwargs):
        msg, *_ = args
        if any(item in str(msg).lower() for item in ("step", "steps", "verify")):
            StepLogs.test_steps.append(msg)
        return func(*args, **kwargs)

    return wrapper


logger = logging.getLogger("pythonLog")
LOG_COLOR = {
    logging.DEBUG: Fore.WHITE,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.RED + Style.BRIGHT
}


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_color = LOG_COLOR.get(record.levelno, Fore.WHITE)
        message = super().format(record)
        return f"{log_color}{message}{Style.RESET_ALL}"


def setup_logging(
        log_level: int = logging.DEBUG,
) -> None:
    """
    Set up logging configuration with both console and file handlers.
    
    Args:
        log_level: The logging level to use
    """

    log_format = '%(asctime)s | %(levelname)s | %(message)s'
    date_format = "%Y-%m-%d %H:%M:%S"

    # Remove existing handlers to prevent duplicate logs
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = ColoredFormatter(log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Replace the info method with our decorated version
    _logger = logger.info

    @record_steps_log
    def log_with_record(*args, **kwargs):
        _logger(*args, **kwargs)

    logger.info = log_with_record


setup_logging()
