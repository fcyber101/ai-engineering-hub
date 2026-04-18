from loguru import logger
import sys
import os


logger.remove()
logger.add(sys.stdout, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")


os.makedirs("logs", exist_ok=True)


logger.add(
    "logs/presentation_agent.log", 
    rotation="10 MB", 
    retention="1 week",  
    level="DEBUG"
)