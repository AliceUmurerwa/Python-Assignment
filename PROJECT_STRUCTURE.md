# Project Structure

## Directory Organization

```
Python Assignment/
│
├── src/                          # Main source code package
│   ├── __init__.py              # Package initialization
│   │
│   ├── core/                    # Core application logic
│   │   ├── __init__.py
│   │   ├── data_loader.py       # CSV data loading with validation
│   │   ├── ideal_function_selector.py  # Least Squares algorithm
│   │   ├── test_mapper.py       # Test data mapping logic
│   │   └── visualization.py     # Bokeh visualization generator
│   │
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   └── models.py            # TrainingData, IdealFunction, TestData
│   │
│   ├── database/                # Database layer
│   │   ├── __init__.py
│   │   └── database.py          # SQLAlchemy ORM models and manager
│   │
│   └── utils/                   # Utilities and helpers
│       ├── __init__.py
│       ├── exceptions.py        # Custom exception classes
│       └── config.py            # Configuration management
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── unit/                    # Unit tests
│   │   ├── __init__.py
│   │   └── test_main.py         # 30+ test cases
│   └── integration/             # Integration tests
│       └── __init__.py
│
├── Data/                        # Input data directory (actual data files)
│   ├── train.csv               # Training data
│   ├── ideal.csv               # 50 ideal functions
│   └── test.csv                # Test data
│
├── output/                      # Output directory
│   └── visualization.html      # Generated visualizations (after running)
│
├── main.py                      # Application entry point
├── ideal_functions.db          # SQLite database (created after running)
│
└── Documentation & Config
    ├── requirements.txt         # Python dependencies
    ├── pytest.ini              # Pytest configuration
    ├── README.md               # Complete documentation
    ├── GETTING_STARTED.md      # Quick start guide
    ├── QUICK_REFERENCE.md      # Command reference
    ├── DEVELOPMENT_GUIDE.md    # Development guidelines
    ├── PROJECT_COMPLETION_SUMMARY.md  # Completion summary
    └── IMPLEMENTATION_VERIFICATION.md # Verification checklist
```

## Module Descriptions

### src/core/
- **data_loader.py**: Classes for loading CSV files
  - `DataLoader` (base class)
  - `TrainingDataLoader`
  - `IdealFunctionLoader`
  - `TestDataLoader`

- **ideal_function_selector.py**: Least Squares algorithm
  - `IdealFunctionSelector` class

- **test_mapper.py**: Test data mapping logic
  - `TestDataMapper` class

- **visualization.py**: Bokeh visualization
  - `Visualizer` class

### src/models/
- **models.py**: Data model classes
  - `TrainingData` dataclass
  - `IdealFunction` dataclass
  - `TestData` dataclass

### src/database/
- **database.py**: Database layer
  - `TrainingDataDB` SQLAlchemy model
  - `IdealFunctionDB` SQLAlchemy model
  - `TestDataDB` SQLAlchemy model
  - `Database` manager class

### src/utils/
- **exceptions.py**: Custom exceptions
  - `DataLoadError`
  - `InvalidDataError`
  - `DatabaseError`
  - `MappingError`
  - `VisualizationError`

- **config.py**: Configuration settings
  - File paths
  - Database URL
  - Algorithm parameters
  - Directory management

## Data Directory

The `Data/` folder contains the input files:
- `train.csv` - Training dataset
- `ideal.csv` - 50 ideal functions
- `test.csv` - Test dataset

## Output Directory

Results are saved to `output/`:
- `visualization.html` - Interactive Bokeh plots

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

# Run tests
pytest tests/ -v
```

## Import Structure

From `main.py`:
```python
from src.database.database import Database
from src.core.data_loader import TrainingDataLoader
from src.core.ideal_function_selector import IdealFunctionSelector
from src.core.test_mapper import TestDataMapper
from src.core.visualization import Visualizer
from src.models.models import TrainingData, IdealFunction, TestData
from src.utils.exceptions import DataLoadError, DatabaseError, MappingError
from src.utils.config import PROJECT_ROOT, DATA_DIR, OUTPUT_DIR
```

## Key Features

✅ **Organized Structure**: Clear separation of concerns
✅ **Modular Design**: Each component is independent
✅ **Type Hints**: 100% type hint coverage
✅ **Documentation**: Comprehensive docstrings
✅ **Testing**: 30+ unit tests
✅ **Configuration**: Centralized settings
✅ **Real Data**: Uses actual data from Data/ folder
