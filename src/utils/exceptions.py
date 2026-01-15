"""
Custom exceptions for the IU CSEMDSPWP01 Python project.
"""


class DataLoadError(Exception):
    """Exception raised when data loading fails."""

    pass


class InvalidDataError(Exception):
    """Exception raised when data validation fails."""

    pass


class DatabaseError(Exception):
    """Exception raised when database operations fail."""

    pass


class MappingError(Exception):
    """Exception raised when test data mapping fails."""

    pass


class VisualizationError(Exception):
    """Exception raised when visualization creation fails."""

    pass
