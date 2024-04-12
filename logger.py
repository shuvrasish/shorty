import logging

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUCCESS = 25

logging.addLevelName(SUCCESS, "SUCCESS")

# Define ANSI escape codes for colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"


class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: BLUE,
        logging.INFO: BLUE,
        logging.WARNING: YELLOW,
        logging.ERROR: RED,
        logging.CRITICAL: RED,
        SUCCESS: GREEN,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, RESET)
        log_message = super().format(record)
        return f"{log_color}{log_message}{RESET}"


colored_formatter = ColoredFormatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


# Set the colored formatter to the logger
console_handler = logging.StreamHandler()
console_handler.setFormatter(colored_formatter)
logger.addHandler(console_handler)


# Add custom success() method to logger
def log_success(self, message, *args, **kwargs):
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, **kwargs)


logging.Logger.success = log_success
