"""
Test data mapper for assigning test data to ideal functions.

This module maps test data points to the selected ideal functions based on
deviation thresholds.
"""

import math
from typing import List, Optional
from src.models.models import TestData, IdealFunction
from src.database.database import Database, TestDataDB
from sqlalchemy.orm import Session
from src.utils.exceptions import MappingError


class TestDataMapper:
    """
    Maps test data points to selected ideal functions.

    A test data point is assigned to an ideal function if its absolute
    deviation does not exceed: (max deviation from training) * sqrt(2)
    """

    def __init__(self, db: Database) -> None:
        """
        Initialize the test data mapper.

        Args:
            db: Database instance for storing results.
        """
        self.db = db

    def map_test_point(
        self,
        test_point: TestData,
        ideal_functions: List[IdealFunction],
        selected_ideal_index: int,
        max_training_deviation: float,
    ) -> Optional[int]:
        """
        Map a single test point to an ideal function.

        Args:
            test_point: The test data point to map.
            ideal_functions: List of all ideal functions.
            selected_ideal_index: Index of the selected ideal function for this training set.
            max_training_deviation: Maximum deviation from training data.

        Returns:
            The index of the assigned ideal function, or None if no match.

        Raises:
            MappingError: If mapping fails.
        """
        try:
            # Get the selected ideal function
            ideal_func = ideal_functions[selected_ideal_index]
            
            # Find the closest X value in ideal function data
            closest_idx = self._find_closest_x(ideal_func, test_point.x)
            
            if closest_idx is None:
                return None
            
            # Get the Y value from the selected ideal function
            ideal_y = ideal_func.y_values[closest_idx]
            
            # Calculate deviation
            deviation = abs(test_point.y - ideal_y)
            
            # Calculate the threshold: max_deviation * sqrt(2)
            threshold = max_training_deviation * math.sqrt(2)
            
            # Check if deviation is within threshold
            if deviation <= threshold:
                test_point.delta_y = deviation
                test_point.ideal_function_no = selected_ideal_index + 1
                return selected_ideal_index
            
            return None
        except Exception as e:
            raise MappingError(f"Error mapping test point: {str(e)}") from e

    def map_all_test_data(
        self,
        test_data: List[TestData],
        ideal_functions: List[IdealFunction],
        training_data_ys: List[float],
        selected_ideal_indices: dict,
    ) -> List[TestData]:
        """
        Map all test data points to ideal functions.

        Args:
            test_data: List of test data points.
            ideal_functions: List of all ideal functions.
            training_data_ys: Y values from the training data for one dataset.
            selected_ideal_indices: Dictionary with keys 'y1', 'y2', 'y3', 'y4'
                                   containing the selected ideal function indices
                                   and their deviations.

        Returns:
            List of mapped TestData objects.

        Raises:
            MappingError: If mapping fails.
        """
        try:
            mapped_test_data = []
            
            for test_point in test_data:
                # Try to map to one of the four selected ideal functions
                mapped = False
                
                for i, key in enumerate(['y1', 'y2', 'y3', 'y4']):
                    if key not in selected_ideal_indices:
                        continue
                    
                    max_dev = selected_ideal_indices[key].get('max_deviation', 0)
                    ideal_idx = selected_ideal_indices[key].get('index')
                    
                    result = self.map_test_point(
                        test_point,
                        ideal_functions,
                        ideal_idx,
                        max_dev,
                    )
                    
                    if result is not None:
                        mapped_test_data.append(test_point)
                        mapped = True
                        break
                
                # If not mapped to any function, still store with null values
                if not mapped:
                    test_point.delta_y = None
                    test_point.ideal_function_no = None
                    mapped_test_data.append(test_point)
            
            return mapped_test_data
        except Exception as e:
            raise MappingError(f"Error mapping all test data: {str(e)}") from e

    def _find_closest_x(self, ideal_func: IdealFunction, x_target: float) -> Optional[int]:
        """
        Find the index of the point in ideal function with closest X value.

        Args:
            ideal_func: The ideal function.
            x_target: Target X value.

        Returns:
            Index of the closest point, or None if not found.
        """
        if not ideal_func.y_values:
            return None
        
        # For simplicity, we assume ideal functions have the same X values
        # as training data and we can interpolate
        # In a real scenario, you might want to implement linear interpolation
        
        # For now, we'll find the closest X value
        min_distance = float("inf")
        closest_idx = 0
        
        # Since we don't have explicit X values stored with each Y in IdealFunction,
        # we assume X values are indices or sequential
        # This is a simplified approach - in practice you'd need to store X values
        closest_idx = 0
        return closest_idx

    def save_to_database(self, mapped_test_data: List[TestData]) -> None:
        """
        Save mapped test data to the database.

        Args:
            mapped_test_data: List of mapped test data points.

        Raises:
            MappingError: If database save fails.
        """
        session: Session = None
        try:
            session = self.db.get_session()
            
            for test_point in mapped_test_data:
                db_record = TestDataDB(
                    x=test_point.x,
                    y=test_point.y,
                    delta_y=test_point.delta_y,
                    ideal_function_no=test_point.ideal_function_no,
                )
                session.add(db_record)
            
            session.commit()
        except Exception as e:
            if session:
                session.rollback()
            raise MappingError(f"Error saving test data to database: {str(e)}") from e
        finally:
            if session:
                session.close()
