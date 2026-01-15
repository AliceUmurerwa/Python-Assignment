"""
Ideal function selector using Least Squares method for the IU CSEMDSPWP01 project.

This module implements the algorithm to select the best matching ideal function
for each training dataset using the least squares method.
"""

import numpy as np
from typing import List, Tuple
from src.models.models import TrainingData, IdealFunction
from src.utils.exceptions import MappingError


class IdealFunctionSelector:
    """
    Selector class for finding best matching ideal functions using Least Squares.

    The Least Squares method calculates the sum of squared deviations between
    training data and each ideal function, and selects the function with the
    minimum deviation.
    """

    @staticmethod
    def calculate_squared_deviations(
        training_y: float, ideal_y: float
    ) -> float:
        """
        Calculate squared deviation between a training point and ideal function point.

        Args:
            training_y: Y value from training data.
            ideal_y: Y value from ideal function.

        Returns:
            Squared deviation.
        """
        return (training_y - ideal_y) ** 2

    @staticmethod
    def sum_squared_deviations(
        training_y_values: List[float], ideal_y_values: List[float]
    ) -> float:
        """
        Calculate the sum of squared deviations between training and ideal data.

        Args:
            training_y_values: List of Y values from training data.
            ideal_y_values: List of Y values from ideal function.

        Returns:
            Sum of squared deviations.

        Raises:
            ValueError: If lists have different lengths.
        """
        if len(training_y_values) != len(ideal_y_values):
            raise ValueError("Training and ideal function lists must have the same length")
        
        return sum(
            IdealFunctionSelector.calculate_squared_deviations(t, i)
            for t, i in zip(training_y_values, ideal_y_values)
        )

    def select_ideal_function(
        self,
        training_data: List[TrainingData],
        ideal_functions: List[IdealFunction],
        training_index: int,
    ) -> Tuple[int, float, List[float]]:
        """
        Select the best matching ideal function for a training dataset.

        Args:
            training_data: List of all training data points.
            ideal_functions: List of all ideal functions.
            training_index: Index of the training dataset to match (0-3 for Y1-Y4).

        Returns:
            Tuple of (ideal_function_index, min_deviation, max_deviations_per_point).
                - ideal_function_index: Index of the selected ideal function (0-49).
                - min_deviation: Sum of squared deviations for the selected function.
                - max_deviations_per_point: List of absolute deviations for each training point.

        Raises:
            MappingError: If selection process fails.
            ValueError: If training_index is out of range.
        """
        if not (0 <= training_index <= 3):
            raise ValueError(f"Training index must be 0-3, got {training_index}")

        try:
            min_deviation = float("inf")
            best_function_index = -1
            deviations_per_point = []

            # For each ideal function, calculate total squared deviation
            for ideal_idx, ideal_func in enumerate(ideal_functions):
                # Extract Y values for the specific training dataset
                training_y_values = [
                    t.y_values[training_index] for t in training_data
                ]

                # Calculate sum of squared deviations
                ssd = self.sum_squared_deviations(training_y_values, ideal_func.y_values)

                # Track the best match
                if ssd < min_deviation:
                    min_deviation = ssd
                    best_function_index = ideal_idx

            # Calculate deviations per point for the selected function
            selected_ideal = ideal_functions[best_function_index]
            training_y_values = [t.y_values[training_index] for t in training_data]
            deviations_per_point = [
                abs(t_y - i_y)
                for t_y, i_y in zip(training_y_values, selected_ideal.y_values)
            ]

            return best_function_index, min_deviation, deviations_per_point

        except Exception as e:
            raise MappingError(f"Error selecting ideal function: {str(e)}") from e

    def select_all_ideal_functions(
        self,
        training_data: List[TrainingData],
        ideal_functions: List[IdealFunction],
    ) -> dict:
        """
        Select the best matching ideal function for all four training datasets.

        Args:
            training_data: List of all training data points.
            ideal_functions: List of all ideal functions.

        Returns:
            Dictionary with keys 'y1', 'y2', 'y3', 'y4' containing:
            - 'index': The selected ideal function index.
            - 'min_deviation': Sum of squared deviations.
            - 'max_deviation': Maximum absolute deviation per point.
            - 'deviations': List of deviations per point.

        Raises:
            MappingError: If selection process fails.
        """
        try:
            results = {}
            for training_idx in range(4):
                func_idx, min_dev, deviations = self.select_ideal_function(
                    training_data, ideal_functions, training_idx
                )
                
                results[f"y{training_idx + 1}"] = {
                    "index": func_idx,
                    "min_deviation": min_dev,
                    "max_deviation": max(deviations) if deviations else 0,
                    "deviations": deviations,
                }
            
            return results
        except Exception as e:
            raise MappingError(f"Error selecting all ideal functions: {str(e)}") from e
