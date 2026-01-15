# IU CSEMDSPWP01 - Programming with Python
## Ideal Function Selector Project

A complete Python application for selecting ideal functions using the Least Squares method and mapping test data to the selected functions.

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

### Usage

#### Step 1: Generate Sample Data (Optional)
```bash
python generate_sample_data.py
```

This creates:
- `train_data_1.csv`: Sample training data
- `ideal_functions.csv`: Sample ideal functions
- `test_data.csv`: Sample test data

#### Step 2: Run the Application
```bash
python main.py
```

#### Expected Output
```
============================================================
IU CSEMDSPWP01 - Ideal Function Selector
============================================================

Loading training data...
  ✓ Loaded training data 1: 100 points
Loading ideal functions...
  ✓ Loaded ideal functions: 100 functions with 50 each
Loading test data...
  ✓ Loaded test data: 50 points

Initializing database...
  ✓ Database initialized
  ✓ Populated training data: 100 records
  ✓ Populated ideal functions: 100 records

Selecting ideal functions using Least Squares...
  ✓ y1: Ideal Function 15, Max Deviation: 0.5234
  ✓ y2: Ideal Function 23, Max Deviation: 0.4891
  ✓ y3: Ideal Function 42, Max Deviation: 0.6123
  ✓ y4: Ideal Function 31, Max Deviation: 0.5567

Mapping test data to ideal functions...
  ✓ Mapped test data: 48/50 points

Generating visualizations...
  ✓ Visualizations saved to visualization.html

============================================================
Application completed successfully!
============================================================
```

#### Step 3: View Results
- Database file: `ideal_functions.db`
- Visualizations: `visualization.html` (open in web browser)

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_main.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
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

#### data_loader.py
CSV data loaders with validation:
- `DataLoader`: Base class with common functionality
- `TrainingDataLoader`: Loads training CSV files
- `IdealFunctionLoader`: Loads ideal functions CSV
- `TestDataLoader`: Loads test data CSV

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

### Code Quality

#### PEP 8 Compliance
- All code follows PEP 8 style guidelines
- Line length limited to ~100 characters
- Proper spacing and naming conventions

#### Type Hints
All functions include type hints for parameters and return values:
```python
def load_csv(file_path: str) -> pd.DataFrame:
    """Load a CSV file into a pandas DataFrame."""
```

#### Documentation
- Comprehensive module docstrings
- Class and method docstrings with Args, Returns, Raises
- Inline comments for complex logic

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | 2.0.3 | Data manipulation and CSV loading |
| numpy | 1.24.3 | Numerical computations |
| sqlalchemy | 2.0.19 | ORM and database management |
| bokeh | 3.3.0 | Interactive visualizations |
| pytest | 7.4.0 | Unit testing framework |

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

### Example Usage

```python
from main import Application

# Create application instance
app = Application("my_database.db")

# Run the complete workflow
app.run(
    training_files=["train1.csv", "train2.csv", "train3.csv", "train4.csv"],
    ideal_file="ideal_functions.csv",
    test_file="test_data.csv"
)

# Access results
for key, value in app.selected_ideal_functions.items():
    print(f"Best function for {key}: {value['index']}")
    print(f"Max deviation: {value['max_deviation']:.4f}")
```

### Troubleshooting

**Issue**: "File not found" error
- **Solution**: Ensure CSV files are in the correct directory or provide absolute paths

**Issue**: SQLAlchemy database locked error
- **Solution**: Close the database with `app.db.close()` after use

**Issue**: Bokeh visualization not opening
- **Solution**: Open the `visualization.html` file manually in a web browser

### Performance Considerations

- **Data Size**: Optimized for datasets with 100-10,000 training points
- **Memory**: Loads all data into memory - adjust for very large datasets
- **Database**: SQLite suitable for datasets up to ~1GB

### Future Enhancements

1. Support for different deviation thresholds
2. Linear interpolation for X values between data points
3. Batch processing for large test datasets
4. Export results to multiple formats (Excel, JSON, etc.)
5. Interactive parameter tuning in visualizations
6. Performance profiling and optimization
7. Parallel processing for ideal function selection

### Author Notes

This project demonstrates:
- Professional Python package structure
- Object-oriented design with inheritance
- Database operations with ORM
- Data processing and analysis
- Scientific computation (Least Squares)
- Testing best practices
- Documentation standards

### License

This project is provided as-is for educational purposes.

---

**Last Updated**: January 15, 2026
**Python Version**: 3.8+
**Status**: Complete and tested
