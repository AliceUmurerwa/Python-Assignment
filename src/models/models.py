"""
Data models for the IU CSEMDSPWP01 Python project.
"""

from typing import List
from dataclasses import dataclass


@dataclass
class TrainingData:
    """
    Represents a single row of training data.

    Attributes:
        x: The input value.
        y_values: List of four Y values (Y1, Y2, Y3, Y4).
    """

    x: float
    y_values: List[float]

    def __post_init__(self) -> None:
        """Validate that exactly 4 Y values are provided."""
        if len(self.y_values) != 4:
            raise ValueError("Training data must have exactly 4 Y values")


@dataclass
class IdealFunction:
    """
    Represents ideal function data.

    In the actual data structure, we have 50 ideal functions across 400 X values.
    Each IdealFunction represents ONE of the 50 ideal functions with values across all X coordinates.

    Attributes:
        x: A reference X value (not used for comparison, included for consistency).
        y_values: List of Y values for this ideal function across all training points (400 values).
    """

    x: float
    y_values: List[float]

    def __post_init__(self) -> None:
        """Validate that Y values are provided."""
        if not self.y_values or len(self.y_values) == 0:
            raise ValueError("Ideal function must have Y values")


@dataclass
class TestData:
    """
    Represents a single row of test data.

    Attributes:
        x: The input value.
        y: The output value.
        delta_y: The allowed deviation.
        ideal_function_no: The assigned ideal function number (0-49).
    """

    x: float
    y: float
    delta_y: float = None
    ideal_function_no: int = None
