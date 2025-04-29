"""
model/da/config.py
------------------
Handles database configuration, initialization, and engine setup.

If the target database doesn't exist, it will be created.
Then tables are initialized based on SQLAlchemy models.

Exports:
- DB_CONFIG      : The configuration dictionary for DB connection.
- engine         : SQLAlchemy engine for the active database.
- Session        : SQLAlchemy sessionmaker bound to engine.
- initialize_database(): Logic for database existence check and initialization.
"""

from typing import Dict
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session as SessionType
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from model.entity.base import Base

# PostgreSQL Database Configuration
DB_CONFIG: Dict[str, str] = {
    "user": "postgres",
    "password": "nikinika",
    "host": "localhost",
    "port": "5432",
    "default_db": "postgres",
    "target_db": "books_borrow",
}


def initialize_database() -> Engine:
    """
    Initialize the target database.
    If it doesn't exist, create it and initialize tables.

    Returns:
        Engine: SQLAlchemy engine connected to the target database.
    """
    try:
        # Connect to default database to check if target DB exists
        temp_engine = create_engine(
            f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
            f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['default_db']}"
        )

        with temp_engine.connect() as conn:
            conn = conn.execution_options(isolation_level="AUTOCOMMIT")
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :dbname"),
                {"dbname": DB_CONFIG["target_db"]},
            ).scalar()

            if not exists:
                conn.execute(text(f"CREATE DATABASE {DB_CONFIG['target_db']}"))
                print(f"✅ Database '{DB_CONFIG['target_db']}' created successfully.")

        # Connect to the target database
        engine = create_engine(
            f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
            f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['target_db']}",
            echo=False,
        )

        # Create tables if not already created
        Base.metadata.create_all(engine)
        print("✅ Tables initialized successfully.")
        return engine

    except SQLAlchemyError as e:
        print(f"❌ Database initialization failed: {e}")
        exit(1)


# Initialize engine and sessionmaker
engine: Engine = initialize_database()
Session: sessionmaker[SessionType] = sessionmaker(bind=engine)
