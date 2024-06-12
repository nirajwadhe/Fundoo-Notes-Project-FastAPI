import logging
from logging.handlers import RotatingFileHandler

# Configure the logger
logger = logging.getLogger("fastapi")
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler("notes/app.log", maxBytes=2000, backupCount=10)
file_handler.setLevel(logging.INFO)

# Create formatters and add them to handlers
console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
