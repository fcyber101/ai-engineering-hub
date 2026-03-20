import sys
import os
from loguru import logger
from datetime import datetime


_LOGGING_INITIALIZED = False

def setup_logging():
    global _LOGGING_INITIALIZED
    
    if _LOGGING_INITIALIZED:
        return
    
    logger.remove()

    dev_format = (
        "<green>{time:HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    )
    prod_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function} | {message}"

    env = os.getenv("ENV_TYPE", "dev").lower()

    if env == "dev":
        logger.add(
            sys.stderr,
            level="DEBUG",
            format=dev_format,
            colorize=True,
            enqueue=False,  
            backtrace=True,
            diagnose=True
        )
        logger.info("Development mode: logging to the console (DEBUG)")

    else:
        logger.add(
            sys.stderr,
            level="INFO",
            format=prod_format,
            colorize=False,
            enqueue=True,
        )
        logger.add(
            f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_app.log",
            level="DEBUG",
            rotation="10 MB",
            retention="1 month",
            compression="zip",
            serialize=False, 
            enqueue=True,
        )
        logger.info("Production mode: logs to console (INFO) + file (DEBUG)")
    
    _LOGGING_INITIALIZED = True