from pathlib import Path
from loguru import logger
import sys


# Root project
BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


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


# App log
logger.add(
    LOG_DIR / "app.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
)


# Error log
logger.add(
    LOG_DIR / "error.log",
    level="ERROR",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
)


# Trade log
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