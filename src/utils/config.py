"""
Configuration module for the IU CSEMDSPWP01 Python project.

This module contains configuration settings for the application.
"""

import os
from typing import List

# Project paths - point to the actual project root (3 levels up from this file)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, "Data")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")

# Database configuration
DATABASE_PATH = os.path.join(PROJECT_ROOT, "ideal_functions.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Data files configuration - using actual data files
TRAINING_FILE: str = os.path.join(DATA_DIR, "train.csv")
IDEAL_FUNCTIONS_FILE: str = os.path.join(DATA_DIR, "ideal.csv")
TEST_DATA_FILE: str = os.path.join(DATA_DIR, "test.csv")
# Output files configuration
VISUALIZATION_OUTPUT: str = os.path.join(OUTPUT_DIR, "visualization.html")
RESULTS_OUTPUT: str = os.path.join(OUTPUT_DIR, "results.json")

# Algorithm configuration
SQRT_2_CONSTANT = 1.4142135623730951  # sqrt(2) for deviation threshold
TRAINING_DATASET_COUNT = 4
IDEAL_FUNCTION_COUNT = 50

# Visualization configuration
PLOT_WIDTH = 800
PLOT_HEIGHT = 400
HOVER_TOOLTIPS = [("X", "@x"), ("Y", "@y")]

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def create_directories() -> None:
    """Create required directories if they don't exist."""
    for directory in [DATA_DIR, OUTPUT_DIR]:
        os.makedirs(directory, exist_ok=True)


# Create directories on import
create_directories()
