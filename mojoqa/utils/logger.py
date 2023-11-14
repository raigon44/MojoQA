"""
This module provides configuration settings for logging in the MojoQA application.
It sets up a logger named 'MojoQA_Log' with an INFO log level and configures a console handler to display log messages on the console.

Author: Raigon Augustin
Date: 14.11.2023
"""

import logging

logger = logging.getLogger('MojoQA_Log')
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(filename='./log/MojoQA.log')
file_handler.setLevel(logging.INFO)

logging_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

console_handler.setFormatter(logging_format)
file_handler.setFormatter(logging_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
