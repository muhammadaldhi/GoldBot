from __future__ import annotations

import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


# =========================
# Logger
# =========================

logger = logging.getLogger(__name__)


# =========================
# Database Config
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(
    exist_ok=True
)

DATABASE_URL = f"sqlite:///{DB_DIR / 'goldbot.db'}"


# =========================
# Base Model
# =========================

class Base(DeclarativeBase):
    """
    Base class untuk semua database model.
    """
    pass


# =========================
# Database Singleton
# =========================

class Database:
    """
    Singleton database manager.
    """

    _instance: Database | None = None

    def __new__(cls) -> Database:
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)

            cls._instance._engine = None
            cls._instance._session_factory = None

        return cls._instance


    def initialize(self) -> None:
        """
        Initialize database connection.
        """

        if self._engine is not None:
            return

        try:
            logger.info("Initializing database...")

            self._engine = create_engine(
                DATABASE_URL,
                echo=False,
                future=True
            )

            self._session_factory = sessionmaker(
    bind=self._engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

            logger.info(
                "Database initialized successfully"
            )

        except Exception as exc:
            logger.exception(
                f"Database initialization failed: {exc}"
            )
            raise


    @property
    def engine(self) -> Engine:
        """
        Return database engine.
        """

        if self._engine is None:
            self.initialize()

        return self._engine


    def create_tables(self) -> None:
        """
        Auto create database tables.
        """

        try:
            Base.metadata.create_all(
                bind=self.engine
            )

            logger.info(
                "Database tables checked"
            )

        except Exception as exc:
            logger.exception(
                f"Create tables failed: {exc}"
            )
            raise


    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """
        Database session manager.

        Example:

            with db.session() as session:
                session.add(data)

        """

        if self._session_factory is None:
            self.initialize()


        session = self._session_factory()

        try:
            yield session
            session.commit()

        except Exception as exc:
            session.rollback()

            logger.exception(
                f"Database transaction failed: {exc}"
            )

            raise

        finally:
            session.close()



# =========================
# Global Database Instance
# =========================

db = Database()