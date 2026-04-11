# Python written assessment
## Ideal function selector project

A complete python application for selecting ideal functions using the Least Squares method and mapping test data to the selected functions.

### Project Overview

This project implements a comprehensive solution for:
1. **Data Loading**: Load training data, ideal functions, and test data from CSV files
2. **Database Management**: Store data in SQLite using SQLAlchemy ORM
3. **Ideal Function Selection**: Use Least Squares method to select the best ideal function for each training dataset
4. **Test Data Mapping**: Assign test data points to ideal functions based on deviation thresholds
5. **Visualization**: Create interactive Bokeh visualizations of results

### Project Structure

```
Python Assignment/
├── main.py                      # Main application orchestrator
├── database.py                  # SQLAlchemy ORM models and database manager
├── models.py                    # Data models (TrainingData, IdealFunction, TestData)
├── data_loader.py              # CSV data loaders with validation
├── ideal_function_selector.py  # Least Squares ideal function selection logic
├── test_mapper.py              # Test data mapping to ideal functions
├── visualization.py            # Bokeh visualization generator
├── exceptions.py               # Custom exceptions
├── requirements.txt            # Python dependencies
├── generate_sample_data.py     # Sample data generator for testing
└── tests/
    └── test_main.py            # Comprehensive unit tests
```

### Features

#### 1. Object-Oriented Design
- **Base Class**: `DataLoader` base class with subclasses `TrainingDataLoader`, `IdealFunctionLoader`, `TestDataLoader`
- **Database Manager**: `Database` class for SQLite operations
- **Selectors & Mappers**: `IdealFunctionSelector` and `TestDataMapper` classes

#### 2. Database Schema
- **training_data**: X, Y1, Y2, Y3, Y4
- **ideal_functions**: X, Y1, Y2, ..., Y50
- **test_data**: X, Y, Delta_Y, Ideal_Function_No

#### 3. Least Squares Algorithm
Selects the ideal function with minimum sum of squared deviations:
```
Deviation = Σ(Training_Y - Ideal_Y)²
```

#### 4. Test Data Mapping
Assigns test data if:
```
|Test_Y - Ideal_Y| ≤ (Max_Training_Deviation × √2)
```

#### 5. Visualizations
- Training data vs selected ideal functions
- Test data with function assignments
- All 50 ideal functions overlay

#### 6. Error Handling
Custom exceptions:
- `DataLoadError`: File loading failures
- `InvalidDataError`: Data validation failures
- `DatabaseError`: Database operation failures
- `MappingError`: Mapping process failures
- `VisualizationError`: Visualization generation failures

### Installation

#### 1. Clone or Download the Project
```bash
cd "Python Assignment"
```

#### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```


### File Descriptions

#### main.py
Main application class that orchestrates the entire workflow:
- Loads data from CSV files
- Initializes database
- Selects ideal functions
- Maps test data
- Generates visualizations

#### database.py
SQLAlchemy ORM models:
- `TrainingDataDB`: Training data table
- `IdealFunctionDB`: Ideal functions table (50 Y columns)
- `TestDataDB`: Test data mapping results
- `Database`: Manager class for database operations

#### models.py
Data models using dataclasses:
- `TrainingData`: Single training data point (4 Y values)
- `IdealFunction`: Single ideal function (50 Y values)
- `TestData`: Single test data point with optional mapping

#### ideal_function_selector.py
Least Squares implementation:
- `calculate_squared_deviations()`: Calculate single deviation
- `sum_squared_deviations()`: Calculate total squared deviation
- `select_ideal_function()`: Select best function for one dataset
- `select_all_ideal_functions()`: Select for all four datasets

#### test_mapper.py
Test data mapping logic:
- `map_test_point()`: Map single test point
- `map_all_test_data()`: Map all test points
- `save_to_database()`: Persist mapped data

#### visualization.py
Bokeh visualization generator:
- `plot_training_data_with_ideal_function()`: Plot training vs ideal
- `plot_test_data_with_assignments()`: Plot test data mappings
- `plot_all_ideal_functions()`: Plot all 50 functions
- `save_visualizations()`: Export to HTML

#### exceptions.py
Custom exception classes:
- `DataLoadError`
- `InvalidDataError`
- `DatabaseError`
- `MappingError`
- `VisualizationError`


### Mathematical Details

#### Least Squares Selection
For each training dataset Y_i, find the ideal function that minimizes:

```
SSD = Σ(Training_Y_j - Ideal_Y_j)²
```

Where:
- j: Index of data point (1 to n)
- n: Number of training points

#### Test Data Mapping Criterion
A test point is assigned to ideal function k if:

```
|Test_Y - Ideal_Y_k| ≤ max_deviation × √2
```

Where:
- max_deviation: Maximum absolute deviation from training data
- √2 ≈ 1.414: Safety factor


### Author

Alice Umurerwa 

