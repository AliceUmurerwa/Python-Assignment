"""
Unit tests for the IU CSEMDSPWP01 Python project.

Tests for data loading, ideal function selection, and database operations.
"""

import pytest
import os
import tempfile
from typing import List

from models import TrainingData, IdealFunction, TestData
from data_loader import TrainingDataLoader, IdealFunctionLoader, TestDataLoader
from ideal_function_selector import IdealFunctionSelector
from database import Database, TrainingDataDB, IdealFunctionDB
from exceptions import DataLoadError, InvalidDataError, DatabaseError


class TestTrainingData:
    """Test suite for TrainingData model."""

    def test_training_data_creation(self):
        """Test creating a TrainingData object."""
        data = TrainingData(x=1.0, y_values=[1.1, 2.2, 3.3, 4.4])
        assert data.x == 1.0
        assert len(data.y_values) == 4
        assert data.y_values[0] == 1.1

    def test_training_data_invalid_y_count(self):
        """Test that TrainingData rejects wrong number of Y values."""
        with pytest.raises(ValueError, match="exactly 4 Y values"):
            TrainingData(x=1.0, y_values=[1.1, 2.2, 3.3])  # Only 3 values


class TestIdealFunction:
    """Test suite for IdealFunction model."""

    def test_ideal_function_creation(self):
        """Test creating an IdealFunction object."""
        y_values = [float(i) for i in range(50)]
        func = IdealFunction(x=1.0, y_values=y_values)
        assert func.x == 1.0
        assert len(func.y_values) == 50

    def test_ideal_function_invalid_y_count(self):
        """Test that IdealFunction rejects wrong number of Y values."""
        with pytest.raises(ValueError, match="exactly 50 Y values"):
            IdealFunction(x=1.0, y_values=[1.0, 2.0])  # Only 2 values


class TestTestData:
    """Test suite for TestData model."""

    def test_test_data_creation(self):
        """Test creating a TestData object."""
        data = TestData(x=1.0, y=2.5)
        assert data.x == 1.0
        assert data.y == 2.5
        assert data.delta_y is None
        assert data.ideal_function_no is None

    def test_test_data_with_assignment(self):
        """Test TestData with assignment values."""
        data = TestData(x=1.0, y=2.5, delta_y=0.5, ideal_function_no=10)
        assert data.delta_y == 0.5
        assert data.ideal_function_no == 10


class TestTrainingDataLoader:
    """Test suite for TrainingDataLoader."""

    def test_load_csv_file_not_found(self):
        """Test error handling for non-existent file."""
        loader = TrainingDataLoader()
        with pytest.raises(DataLoadError, match="File not found"):
            loader.load_csv("nonexistent_file.csv")

    def test_validate_dataframe_missing_columns(self):
        """Test validation of DataFrame columns."""
        import pandas as pd

        loader = TrainingDataLoader()
        df = pd.DataFrame({"x": [1, 2], "y1": [1, 2]})  # Missing y2, y3, y4
        
        with pytest.raises(InvalidDataError, match="Missing columns"):
            loader.validate_dataframe(df, ["x", "y1", "y2", "y3", "y4"])

    def test_create_sample_training_csv(self):
        """Test loading sample training data."""
        loader = TrainingDataLoader()
        
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("x,y1,y2,y3,y4\n")
            f.write("1.0,1.1,1.2,1.3,1.4\n")
            f.write("2.0,2.1,2.2,2.3,2.4\n")
            temp_file = f.name
        
        try:
            training_data, df = loader.load_training_data(temp_file)
            assert len(training_data) == 2
            assert training_data[0].x == 1.0
            assert len(training_data[0].y_values) == 4
        finally:
            os.unlink(temp_file)


class TestIdealFunctionLoader:
    """Test suite for IdealFunctionLoader."""

    def test_create_sample_ideal_csv(self):
        """Test loading sample ideal functions."""
        loader = IdealFunctionLoader()
        
        # Create a temporary CSV file with 50 Y columns
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            columns = ["x"] + [f"y{i}" for i in range(1, 51)]
            f.write(",".join(columns) + "\n")
            
            values = ["1.0"] + [f"{i}.{j}" for i in range(1, 51) for j in range(1, 2)]
            f.write(",".join(values[:51]) + "\n")  # x + 50 y values
            
            temp_file = f.name
        
        try:
            ideal_data, df = loader.load_ideal_functions(temp_file)
            assert len(ideal_data) == 1
            assert ideal_data[0].x == 1.0
            assert len(ideal_data[0].y_values) == 50
        finally:
            os.unlink(temp_file)


class TestIdealFunctionSelector:
    """Test suite for IdealFunctionSelector."""

    def test_calculate_squared_deviations(self):
        """Test squared deviation calculation."""
        selector = IdealFunctionSelector()
        deviation = selector.calculate_squared_deviations(5.0, 3.0)
        assert deviation == 4.0  # (5-3)^2 = 4

    def test_sum_squared_deviations(self):
        """Test sum of squared deviations."""
        selector = IdealFunctionSelector()
        training_y = [1.0, 2.0, 3.0]
        ideal_y = [1.1, 2.1, 3.1]
        ssd = selector.sum_squared_deviations(training_y, ideal_y)
        expected = 0.1**2 + 0.1**2 + 0.1**2
        assert abs(ssd - expected) < 0.0001

    def test_sum_squared_deviations_length_mismatch(self):
        """Test error when lists have different lengths."""
        selector = IdealFunctionSelector()
        with pytest.raises(ValueError, match="same length"):
            selector.sum_squared_deviations([1.0, 2.0], [1.0, 2.0, 3.0])

    def test_select_ideal_function_simple(self):
        """Test ideal function selection with simple data."""
        selector = IdealFunctionSelector()
        
        # Create simple training data
        training_data = [
            TrainingData(x=1.0, y_values=[1.0, 2.0, 3.0, 4.0]),
            TrainingData(x=2.0, y_values=[2.0, 3.0, 4.0, 5.0]),
        ]
        
        # Create ideal functions - one is perfect match for Y1
        ideal_functions = [
            IdealFunction(x=1.5, y_values=[1.0, 2.0] + [0.0] * 48),  # Perfect for Y1
            IdealFunction(x=1.5, y_values=[5.0, 6.0] + [0.0] * 48),  # Bad for Y1
        ]
        
        ideal_idx, min_dev, deviations = selector.select_ideal_function(
            training_data, ideal_functions, 0  # Select for Y1
        )
        
        assert ideal_idx == 0  # First function should be selected
        assert min_dev == 0.0  # Perfect match
        assert all(d == 0.0 for d in deviations)


class TestDatabase:
    """Test suite for Database class."""

    def test_database_initialization(self):
        """Test database initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "test.db")
            db = Database(db_path)
            db.init_db()
            
            assert os.path.exists(db_path)
            assert db.engine is not None
            assert db.Session is not None
            
            db.close()

    def test_database_session_creation(self):
        """Test creating database sessions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "test.db")
            db = Database(db_path)
            db.init_db()
            
            session = db.get_session()
            assert session is not None
            session.close()
            
            db.close()

    def test_database_session_without_init(self):
        """Test error when getting session without initialization."""
        db = Database(":memory:")
        with pytest.raises(DatabaseError, match="not initialized"):
            db.get_session()

    def test_database_insert_and_retrieve(self):
        """Test inserting and retrieving data from database."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "test.db")
            db = Database(db_path)
            db.init_db()
            
            # Insert training data
            session = db.get_session()
            try:
                record = TrainingDataDB(x=1.0, y1=1.1, y2=2.1, y3=3.1, y4=4.1)
                session.add(record)
                session.commit()
                
                # Retrieve
                retrieved = session.query(TrainingDataDB).filter_by(x=1.0).first()
                assert retrieved is not None
                assert retrieved.y1 == 1.1
            finally:
                session.close()
                db.close()


class TestExceptions:
    """Test suite for custom exceptions."""

    def test_data_load_error(self):
        """Test DataLoadError exception."""
        with pytest.raises(DataLoadError):
            raise DataLoadError("Test error")

    def test_invalid_data_error(self):
        """Test InvalidDataError exception."""
        with pytest.raises(InvalidDataError):
            raise InvalidDataError("Test error")

    def test_database_error(self):
        """Test DatabaseError exception."""
        with pytest.raises(DatabaseError):
            raise DatabaseError("Test error")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
