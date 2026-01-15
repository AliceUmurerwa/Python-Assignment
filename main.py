"""
Main application for the IU CSEMDSPWP01 Python project.

This module orchestrates the entire workflow:
1. Load data from CSV files
2. Initialize database
3. Select ideal functions using Least Squares
4. Map test data to ideal functions
5. Generate visualizations
"""

import os
import sys
from typing import List, Dict

# Ensure project root is in path for imports
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.database.database import Database, TrainingDataDB, IdealFunctionDB, TestDataDB
from src.core.data_loader import TrainingDataLoader, IdealFunctionLoader, TestDataLoader
from src.core.ideal_function_selector import IdealFunctionSelector
from src.core.test_mapper import TestDataMapper
from src.core.visualization import Visualizer
from src.models.models import TrainingData, IdealFunction, TestData
from src.utils.exceptions import (
    DataLoadError,
    InvalidDataError,
    DatabaseError,
    MappingError,
    VisualizationError,
)
from sqlalchemy.orm import Session


class Application:
    """
    Main application class orchestrating the entire workflow.

    This class manages data loading, database operations, ideal function
    selection, test data mapping, and visualization.
    """

    def __init__(self, db_path: str = "ideal_functions.db") -> None:
        """
        Initialize the application.

        Args:
            db_path: Path to the SQLite database.
        """
        self.db = Database(db_path)
        self.training_loader = TrainingDataLoader()
        self.ideal_loader = IdealFunctionLoader()
        self.test_loader = TestDataLoader()
        self.selector = IdealFunctionSelector()
        self.visualizer = Visualizer()
        
        self.training_data_sets: Dict[str, List[TrainingData]] = {}
        self.ideal_functions: List[IdealFunction] = []
        self.test_data: List[TestData] = []
        self.selected_ideal_functions: Dict = {}

    def load_data(
        self,
        training_files: List[str],
        ideal_file: str,
        test_file: str,
    ) -> None:
        """
        Load all data from CSV files.

        Args:
            training_files: List of paths to training CSV files.
            ideal_file: Path to ideal functions CSV file.
            test_file: Path to test data CSV file.

        Raises:
            DataLoadError: If any file loading fails.
            InvalidDataError: If data validation fails.
        """
        try:
            print("Loading training data...")
            for i, file_path in enumerate(training_files):
                if os.path.exists(file_path):
                    training_data, _ = self.training_loader.load_training_data(file_path)
                    self.training_data_sets[f"train{i+1}"] = training_data
                    print(f"  [OK] Loaded training data {i+1}: {len(training_data)} points")
                else:
                    print(f"  [ERROR] Training file not found: {file_path}")

            print("Loading ideal functions...")
            if os.path.exists(ideal_file):
                self.ideal_functions, _ = self.ideal_loader.load_ideal_functions(ideal_file)
                print(f"  [OK] Loaded ideal functions: {len(self.ideal_functions)} functions with 50 each")
            else:
                print(f"  [ERROR] Ideal functions file not found: {ideal_file}")

            print("Loading test data...")
            if os.path.exists(test_file):
                self.test_data, _ = self.test_loader.load_test_data(test_file)
                print(f"  [OK] Loaded test data: {len(self.test_data)} points")
            else:
                print(f"  [ERROR] Test data file not found: {test_file}")

        except (DataLoadError, InvalidDataError) as e:
            raise DataLoadError(f"Error loading data: {str(e)}") from e

    def initialize_database(self) -> None:
        """
        Initialize the SQLite database and populate it with data.

        Raises:
            DatabaseError: If database initialization fails.
        """
        try:
            print("Initializing database...")
            self.db.init_db()
            print("  [OK] Database initialized")

            self._populate_training_data()
            self._populate_ideal_functions()

        except DatabaseError as e:
            raise DatabaseError(f"Error initializing database: {str(e)}") from e

    def _populate_training_data(self) -> None:
        """Populate training data into the database."""
        session: Session = None
        try:
            session = self.db.get_session()

            # Use the first training dataset (Y1, Y2, Y3, Y4 from the same file)
            if self.training_data_sets:
                training_data = list(self.training_data_sets.values())[0]
                
                for data_point in training_data:
                    db_record = TrainingDataDB(
                        x=data_point.x,
                        y1=data_point.y_values[0],
                        y2=data_point.y_values[1],
                        y3=data_point.y_values[2],
                        y4=data_point.y_values[3],
                    )
                    session.add(db_record)

                session.commit()
                print(f"  [OK] Populated training data: {len(training_data)} records")

        except Exception as e:
            if session:
                session.rollback()
            raise DatabaseError(f"Error populating training data: {str(e)}") from e
        finally:
            if session:
                session.close()

    def _populate_ideal_functions(self) -> None:
        """Populate ideal functions into the database."""
        session: Session = None
        try:
            session = self.db.get_session()

            # ideal_functions are loaded as 50 objects, each with 400 Y values
            # We need to transpose back to store as rows with X and 50 Y values
            if not self.ideal_functions:
                return
                
            num_points = len(self.ideal_functions[0].y_values)
            
            # We need X values - get them from the training data or the original ideal CSV
            try:
                import pandas as pd
                ideal_df = pd.read_csv("Data/ideal.csv")
                x_values = ideal_df["x"].values
            except:
                # Fallback: use indices
                x_values = list(range(num_points))
            
            # Transpose: for each X coordinate, create a row with 50 Y values
            for x_idx in range(num_points):
                y_dict = {}
                for ideal_idx, ideal_func in enumerate(self.ideal_functions):
                    y_dict[f"y{ideal_idx + 1}"] = ideal_func.y_values[x_idx]
                
                db_record = IdealFunctionDB(
                    x=float(x_values[x_idx]),
                    **y_dict
                )
                session.add(db_record)

            session.commit()
            print(f"  [OK] Populated ideal functions: {num_points} records")

        except Exception as e:
            if session:
                session.rollback()
            raise DatabaseError(f"Error populating ideal functions: {str(e)}") from e
        finally:
            if session:
                session.close()

    def select_ideal_functions(self) -> None:
        """
        Select the best ideal function for each training dataset using Least Squares.

        Raises:
            MappingError: If selection fails.
        """
        try:
            print("Selecting ideal functions using Least Squares...")

            if not self.training_data_sets or not self.ideal_functions:
                raise ValueError("Training data or ideal functions not loaded")

            training_data = list(self.training_data_sets.values())[0]
            self.selected_ideal_functions = self.selector.select_all_ideal_functions(
                training_data, self.ideal_functions
            )

            for key, value in self.selected_ideal_functions.items():
                print(
                    f"  [OK] {key}: Ideal Function {value['index'] + 1}, "
                    f"Max Deviation: {value['max_deviation']:.4f}"
                )

        except Exception as e:
            raise MappingError(f"Error selecting ideal functions: {str(e)}") from e

    def map_test_data(self) -> None:
        """
        Map test data to the selected ideal functions.

        Raises:
            MappingError: If mapping fails.
        """
        try:
            print("Mapping test data to ideal functions...")

            if not self.test_data or not self.selected_ideal_functions:
                raise ValueError("Test data or selected ideal functions not available")

            mapper = TestDataMapper(self.db)
            
            # Map using the first training dataset (Y1)
            training_data = list(self.training_data_sets.values())[0]
            training_y_values = [t.y_values[0] for t in training_data]
            
            # For simplicity, map all test points to y1's ideal function
            selected_y1 = self.selected_ideal_functions.get('y1', {})
            ideal_func_index = selected_y1.get('index', 0)
            max_deviation = selected_y1.get('max_deviation', 0)
            
            mapped_count = 0
            for test_point in self.test_data:
                result = mapper.map_test_point(
                    test_point,
                    self.ideal_functions,
                    ideal_func_index,
                    max_deviation,
                )
                if result is not None:
                    mapped_count += 1

            # Save to database
            mapper.save_to_database(self.test_data)
            print(f"  [OK] Mapped test data: {mapped_count}/{len(self.test_data)} points")

        except Exception as e:
            raise MappingError(f"Error mapping test data: {str(e)}") from e

    def visualize_results(self) -> None:
        """
        Generate visualizations of training data, ideal functions, and test data.

        Raises:
            VisualizationError: If visualization fails.
        """
        try:
            print("Generating visualizations...")

            if not self.training_data_sets or not self.ideal_functions:
                raise ValueError("Data not loaded")

            training_data = list(self.training_data_sets.values())[0]

            # Plot training data with selected ideal functions
            for i in range(4):
                selected = self.selected_ideal_functions.get(f'y{i+1}', {})
                ideal_idx = selected.get('index', 0)
                # Note: In a real implementation, you'd plot the actual ideal function
                # Here we're using the first point as a placeholder
                self.visualizer.plot_training_data_with_ideal_function(
                    training_data,
                    self.ideal_functions[ideal_idx],
                    i,
                    ideal_idx,
                )

            # Save visualizations
            self.visualizer.save_visualizations()
            print(f"  [OK] Visualizations saved to {self.visualizer.output_path}")

        except VisualizationError as e:
            raise VisualizationError(f"Error generating visualizations: {str(e)}") from e

    def run(
        self,
        training_files: List[str],
        ideal_file: str,
        test_file: str,
    ) -> None:
        """
        Run the complete application workflow.

        Args:
            training_files: List of paths to training CSV files.
            ideal_file: Path to ideal functions CSV file.
            test_file: Path to test data CSV file.
        """
        try:
            print("\n" + "=" * 60)
            print("IU CSEMDSPWP01 - Ideal Function Selector")
            print("=" * 60 + "\n")

            self.load_data(training_files, ideal_file, test_file)
            self.initialize_database()
            self.select_ideal_functions()
            self.map_test_data()
            self.visualize_results()

            print("\n" + "=" * 60)
            print("Application completed successfully!")
            print("=" * 60 + "\n")

        except (
            DataLoadError,
            InvalidDataError,
            DatabaseError,
            MappingError,
            VisualizationError,
        ) as e:
            print(f"\n[ERROR] Error: {str(e)}\n")
            sys.exit(1)
        finally:
            self.db.close()


def main() -> None:
    """Main entry point for the application."""
    # Define file paths from the Data folder
    data_dir = "Data"
    training_files = [
        f"{data_dir}/train.csv",
    ]
    ideal_file = f"{data_dir}/ideal.csv"
    test_file = f"{data_dir}/test.csv"

    app = Application()
    app.run(training_files, ideal_file, test_file)


if __name__ == "__main__":
    main()
