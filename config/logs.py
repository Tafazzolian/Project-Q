from loguru import logger
import sys

# from loguru import logger as base_logger

# cache_logger = base_logger.bind(name="cache")
# cache_logger.add("logs/cache_logs.log", level="CRITICAL", rotation="1 week", retention="1 month")

# Configure a logger for INFO level messages and above
logger.add("logs/info_{time}.log", rotation="1 MB", retention="7 days", level="INFO")


# # Configure a separate logger for WARNING level messages and above
# logger.add("logs/warning_{time}.log", rotation="1 week", retention="1 month", level="WARNING")

# # Configure a separate logger for ERROR level messages and above
# logger.add("logs/error_{time}.log", rotation="1 week", retention="1 month", level="ERROR")

# # Configure a separate logger for CRITICAL level messages and above
# logger.add("logs/critical_{time}.log", rotation="1 week", retention="1 month", level="CRITICAL")

# # Optionally, add a logger to stderr for WARNING and above messages, with a different format
# logger.add(sys.stderr, level="WARNING", format="<red>{time}</red> <level>{message}</level>")

__all__ = ["logger"]