from dataclasses import dataclass


@dataclass
class AppConfig:
    APP_NAME: str = "GoldBot"
    VERSION: str = "1.0.0"

    HOST: str = "0.0.0.0"
    PORT: int = 5000
    DEBUG: bool = True


@dataclass
class TradingConfig:
    SYMBOL: str = "XAUUSD"

    TIMEFRAME_ENTRY: str = "M1"
    TIMEFRAME_CONFIRM: str = "M5"
    TIMEFRAME_SETUP: str = "M15"
    TIMEFRAME_TREND: str = "H1"

    MAGIC_NUMBER: int = 20260710

    MAX_SPREAD: int = 30

    MAX_OPEN_TRADES: int = 1

    RISK_PERCENT: float = 1.0

    RR_RATIO: float = 2.0

    USE_BREAK_EVEN: bool = True

    USE_TRAILING_STOP: bool = True


@dataclass
class NewsConfig:
    ENABLED: bool = True

    MINUTES_BEFORE: int = 30

    MINUTES_AFTER: int = 30


@dataclass
class SessionConfig:
    ENABLED: bool = True

    START_HOUR: int = 13

    END_HOUR: int = 23


@dataclass
class DatabaseConfig:
    DATABASE_URL = "sqlite:///data/goldbot.db"


@dataclass
class TelegramConfig:
    ENABLED: bool = False

    TOKEN: str = ""

    CHAT_ID: str = ""


app = AppConfig()

trading = TradingConfig()

news = NewsConfig()

session = SessionConfig()

database = DatabaseConfig()

telegram = TelegramConfig()