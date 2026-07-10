from pathlib import Path
from loguru import logger
import sys


# Folder logs
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


# Hapus handler bawaan
logger.remove()


# Console
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
           "{message}",
)


# App Log
logger.add(
    LOG_DIR / "app.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
)


# Error Log
logger.add(
    LOG_DIR / "error.log",
    level="ERROR",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
)


# Trade Log
logger.add(
    LOG_DIR / "trade.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    filter=lambda record: record["extra"].get("trade", False),
)


def get_logger():
    return logger


def trade_logger():
    return logger.bind(trade=True)