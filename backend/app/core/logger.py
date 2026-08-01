import logging
import sys
import os

def setup_logging():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    environment = os.getenv("ENVIRONMENT", "development")
    
    logging.basicConfig(
        level=logging.DEBUG if environment == "development" else logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
