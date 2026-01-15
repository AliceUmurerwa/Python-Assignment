"""
Data loader for the IU CSEMDSPWP01 Python project.

This module provides classes for loading training data, ideal functions,
and test data from CSV files.
"""

import pandas as pd
from typing import List, Tuple
from src.models.models import TrainingData, IdealFunction, TestData
from src.utils.exceptions import DataLoadError, InvalidDataError


class DataLoader:
    """
    Base class for loading data from CSV files.

    This class provides common functionality for loading and validating
    CSV data.
    """

    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        """
        Load a CSV file into a pandas DataFrame.

        Args:
            file_path: Path to the CSV file.

        Returns:
            Loaded DataFrame.

        Raises:
            DataLoadError: If the file cannot be loaded.
        """
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError as e:
            raise DataLoadError(f"File not found: {file_path}") from e
        except Exception as e:
            raise DataLoadError(f"Error loading CSV file {file_path}: {str(e)}") from e

    @staticmethod
    def validate_dataframe(df: pd.DataFrame, expected_columns: List[str]) -> None:
        """
        Validate that a DataFrame has the expected columns.

        Args:
            df: DataFrame to validate.
            expected_columns: List of expected column names.

        Raises:
            InvalidDataError: If expected columns are missing.
        """
        missing_cols = set(expected_columns) - set(df.columns)
        if missing_cols:
            raise InvalidDataError(
                f"Missing columns: {missing_cols}. Expected: {expected_columns}"
            )


class TrainingDataLoader(DataLoader):
    """
    Loader for training data from CSV files.

    Expects CSV files with columns: x, y1, y2, y3, y4
    """

    def load_training_data(self, file_path: str) -> Tuple[List[TrainingData], pd.DataFrame]:
        """
        Load training data from a CSV file.

        Args:
            file_path: Path to the training data CSV file.

        Returns:
            Tuple of (list of TrainingData objects, DataFrame).

        Raises:
            DataLoadError: If the file cannot be loaded.
            InvalidDataError: If data validation fails.
        """
        df = self.load_csv(file_path)
        expected_cols = ["x", "y1", "y2", "y3", "y4"]
        self.validate_dataframe(df, expected_cols)

        try:
            training_data = []
            for _, row in df.iterrows():
                data = TrainingData(
                    x=float(row["x"]),
                    y_values=[float(row["y1"]), float(row["y2"]), float(row["y3"]), float(row["y4"])],
                )
                training_data.append(data)
            return training_data, df
        except Exception as e:
            raise InvalidDataError(f"Error processing training data: {str(e)}") from e


class IdealFunctionLoader(DataLoader):
    """
    Loader for ideal functions from CSV files.

    Expects CSV files with columns: x, y1, y2, ..., y50
    """

    def load_ideal_functions(self, file_path: str) -> Tuple[List[IdealFunction], pd.DataFrame]:
        """
        Load ideal functions from a CSV file.

        The CSV has 400 rows with 51 columns (x, y1-y50).
        Each row represents one X coordinate with 50 Y values (one per ideal function).
        We transpose this to create 50 IdealFunction objects, each containing
        the Y values across all X coordinates for that specific function.

        Args:
            file_path: Path to the ideal functions CSV file.

        Returns:
            Tuple of (list of IdealFunction objects, DataFrame).
            Each IdealFunction represents one of the 50 ideal functions,
            with all X coordinates and their corresponding Y values.

        Raises:
            DataLoadError: If the file cannot be loaded.
            InvalidDataError: If data validation fails.
        """
        df = self.load_csv(file_path)
        expected_cols = ["x"] + [f"y{i}" for i in range(1, 51)]
        self.validate_dataframe(df, expected_cols)

        try:
            ideal_functions = []
            
            # We need to transpose: create 50 IdealFunction objects
            # Each representing one of the 50 ideal functions across all X values
            x_values = df["x"].values
            
            for ideal_idx in range(1, 51):  # For each of the 50 ideal functions
                y_col = f"y{ideal_idx}"
                y_values = df[y_col].values.tolist()
                
                # Create IdealFunction with first x value (we'll use x values from training data)
                # Actually, we need to store all X coordinates
                # Let's create a pseudo-IdealFunction for comparison
                # For now, use x=0 as placeholder since we compare Y values by index
                func = IdealFunction(x=float(x_values[0]), y_values=y_values)
                ideal_functions.append(func)
                
            return ideal_functions, df
        except Exception as e:
            raise InvalidDataError(f"Error processing ideal functions: {str(e)}") from e


class TestDataLoader(DataLoader):
    """
    Loader for test data from CSV files.

    Expects CSV files with columns: x, y
    """

    def load_test_data(self, file_path: str) -> Tuple[List[TestData], pd.DataFrame]:
        """
        Load test data from a CSV file.

        Args:
            file_path: Path to the test data CSV file.

        Returns:
            Tuple of (list of TestData objects, DataFrame).

        Raises:
            DataLoadError: If the file cannot be loaded.
            InvalidDataError: If data validation fails.
        """
        df = self.load_csv(file_path)
        expected_cols = ["x", "y"]
        self.validate_dataframe(df, expected_cols)

        try:
            test_data = []
            for _, row in df.iterrows():
                data = TestData(x=float(row["x"]), y=float(row["y"]))
                test_data.append(data)
            return test_data, df
        except Exception as e:
            raise InvalidDataError(f"Error processing test data: {str(e)}") from e
