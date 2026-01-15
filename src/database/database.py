"""
Database models using SQLAlchemy ORM for the IU CSEMDSPWP01 Python project.
"""

from sqlalchemy import create_engine, Column, Integer, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
import os

Base = declarative_base()


class TrainingDataDB(Base):
    """
    SQLAlchemy ORM model for training data.

    Attributes:
        id: Primary key.
        x: Input value.
        y1, y2, y3, y4: Output values for the four training datasets.
    """

    __tablename__ = "training_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Float, nullable=False, unique=True)
    y1 = Column(Float, nullable=False)
    y2 = Column(Float, nullable=False)
    y3 = Column(Float, nullable=False)
    y4 = Column(Float, nullable=False)


class IdealFunctionDB(Base):
    """
    SQLAlchemy ORM model for ideal functions.

    Attributes:
        id: Primary key.
        x: Input value.
        y1 to y50: Output values for the 50 ideal functions.
    """

    __tablename__ = "ideal_functions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Float, nullable=False, unique=True)
    y1 = Column(Float, nullable=False)
    y2 = Column(Float, nullable=False)
    y3 = Column(Float, nullable=False)
    y4 = Column(Float, nullable=False)
    y5 = Column(Float, nullable=False)
    y6 = Column(Float, nullable=False)
    y7 = Column(Float, nullable=False)
    y8 = Column(Float, nullable=False)
    y9 = Column(Float, nullable=False)
    y10 = Column(Float, nullable=False)
    y11 = Column(Float, nullable=False)
    y12 = Column(Float, nullable=False)
    y13 = Column(Float, nullable=False)
    y14 = Column(Float, nullable=False)
    y15 = Column(Float, nullable=False)
    y16 = Column(Float, nullable=False)
    y17 = Column(Float, nullable=False)
    y18 = Column(Float, nullable=False)
    y19 = Column(Float, nullable=False)
    y20 = Column(Float, nullable=False)
    y21 = Column(Float, nullable=False)
    y22 = Column(Float, nullable=False)
    y23 = Column(Float, nullable=False)
    y24 = Column(Float, nullable=False)
    y25 = Column(Float, nullable=False)
    y26 = Column(Float, nullable=False)
    y27 = Column(Float, nullable=False)
    y28 = Column(Float, nullable=False)
    y29 = Column(Float, nullable=False)
    y30 = Column(Float, nullable=False)
    y31 = Column(Float, nullable=False)
    y32 = Column(Float, nullable=False)
    y33 = Column(Float, nullable=False)
    y34 = Column(Float, nullable=False)
    y35 = Column(Float, nullable=False)
    y36 = Column(Float, nullable=False)
    y37 = Column(Float, nullable=False)
    y38 = Column(Float, nullable=False)
    y39 = Column(Float, nullable=False)
    y40 = Column(Float, nullable=False)
    y41 = Column(Float, nullable=False)
    y42 = Column(Float, nullable=False)
    y43 = Column(Float, nullable=False)
    y44 = Column(Float, nullable=False)
    y45 = Column(Float, nullable=False)
    y46 = Column(Float, nullable=False)
    y47 = Column(Float, nullable=False)
    y48 = Column(Float, nullable=False)
    y49 = Column(Float, nullable=False)
    y50 = Column(Float, nullable=False)


class TestDataDB(Base):
    """
    SQLAlchemy ORM model for test data mapping results.

    Attributes:
        id: Primary key.
        x: Input value.
        y: Output value.
        delta_y: Deviation from the assigned ideal function.
        ideal_function_no: Index of the assigned ideal function (1-50).
    """

    __tablename__ = "test_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    delta_y = Column(Float, nullable=True)
    ideal_function_no = Column(Integer, nullable=True)


class Database:
    """
    Database manager class for SQLite database operations.

    This class handles database initialization, session management,
    and provides methods for interacting with the database.
    """

    def __init__(self, db_path: str = "ideal_functions.db") -> None:
        """
        Initialize the database manager.

        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self.engine = None
        self.Session = None

    def init_db(self) -> None:
        """
        Initialize the database and create all tables.

        Raises:
            DatabaseError: If database initialization fails.
        """
        try:
            db_url = f"sqlite:///{os.path.abspath(self.db_path)}"
            self.engine = create_engine(db_url, echo=False)
            # Drop all existing tables to ensure clean state
            Base.metadata.drop_all(self.engine)
            # Create all tables fresh
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            from src.utils.exceptions import DatabaseError

            raise DatabaseError(f"Failed to initialize database: {str(e)}")

    def get_session(self) -> Session:
        """
        Get a new database session.

        Returns:
            SQLAlchemy Session object.

        Raises:
            DatabaseError: If engine is not initialized.
        """
        if self.engine is None:
            from src.utils.exceptions import DatabaseError

            raise DatabaseError("Database not initialized. Call init_db() first.")
        return self.Session()

    def close(self) -> None:
        """Close the database connection."""
        if self.engine:
            self.engine.dispose()

    def clear_all_tables(self) -> None:
        """Clear all data from all tables."""
        session = self.get_session()
        try:
            session.query(TestDataDB).delete()
            session.query(IdealFunctionDB).delete()
            session.query(TrainingDataDB).delete()
            session.commit()
        finally:
            session.close()
