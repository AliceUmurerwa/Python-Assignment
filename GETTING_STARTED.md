# Getting Started - IU CSEMDSPWP01 Python Project

## Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Setup

#### 1. Navigate to Project Directory
```bash
cd "C:\Users\25078\Desktop\Python Assignment"
```

#### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
```

#### 3. Activate Virtual Environment
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### Running the Application

The project uses data files from the `Data/` folder:
- `train.csv` - Training data
- `ideal.csv` - 50 ideal functions
- `test.csv` - Test data

#### Run the Application
```bash
python main.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_main.py -v

# Run specific test function
pytest tests/unit/test_main.py::TestTrainingData::test_training_data_creation -v
```

### Expected Output

When you run `python main.py`, you should see:

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
  ✓ Visualizations saved to output/visualization.html

============================================================
Application completed successfully!
============================================================
```

### Viewing Results

1. **SQLite Database**: `ideal_functions.db`
   - Can be opened with SQLite tools or Python

2. **Visualizations**: `output/visualization.html`
   - Open in any web browser

3. **Console Output**: Shows selected ideal functions and mapping statistics

### CSV File Formats

#### Training Data (Data/train.csv)
```
x,y1,y2,y3,y4
1.0,1.1,1.2,1.3,1.4
2.0,2.1,2.2,2.3,2.4
...
```

#### Ideal Functions (Data/ideal.csv)
```
x,y1,y2,...,y50
1.0,0.841,0.540,...,1.234
2.0,0.909,0.416,...,1.567
...
```

#### Test Data (Data/test.csv)
```
x,y
1.0,1.1
2.0,2.1
...
```

### File Structure After Running

```
Python Assignment/
├── src/                          # Source code directory
│   ├── __init__.py
│   ├── core/                     # Core application logic
│   │   ├── __init__.py
│   │   ├── data_loader.py
│   │   ├── ideal_function_selector.py
│   │   ├── test_mapper.py
│   │   └── visualization.py
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   └── models.py
│   ├── database/                 # Database layer
│   │   ├── __init__.py
│   │   └── database.py
│   └── utils/                    # Utilities
│       ├── __init__.py
│       ├── exceptions.py
│       └── config.py
│
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   │   ├── __init__.py
│   │   └── test_main.py
│   └── integration/              # Integration tests
│       └── __init__.py
│
├── Data/                         # Input data directory
│   ├── train.csv                 # Training data
│   ├── ideal.csv                 # Ideal functions
│   └── test.csv                  # Test data
│
├── output/                       # Output directory
│   └── visualization.html        # Generated visualizations
│
├── main.py                       # Main entry point
├── ideal_functions.db            # SQLite database (after running)
├── requirements.txt              # Dependencies
├── pytest.ini                    # Test configuration
├── README.md                     # Full documentation
├── GETTING_STARTED.md           # This file
├── DEVELOPMENT_GUIDE.md         # Development guidelines
├── QUICK_REFERENCE.md           # Quick reference
└── PROJECT_COMPLETION_SUMMARY.md # Completion summary
```

### Troubleshooting

**Problem**: ImportError when running main.py
```
ModuleNotFoundError: No module named 'pandas'
```
**Solution**: Make sure you've installed dependencies
```bash
pip install -r requirements.txt
```

**Problem**: FileNotFoundError for CSV files
```
File not found: train_data_1.csv
```
**Solution**: Run the sample data generator first
```bash
python generate_sample_data.py
```

**Problem**: SQLAlchemy database error
```
sqlalchemy.exc.OperationalError
```
**Solution**: Delete `ideal_functions.db` and run again to reinitialize

**Problem**: Bokeh visualization not opening
```
File 'visualization.html' created but won't open
```
**Solution**: Manually open the file in your browser by double-clicking it

### Project Architecture

```
Application Flow:
1. Data Loading (CSV files)
   ↓
2. Database Initialization (SQLite)
   ↓
3. Ideal Function Selection (Least Squares)
   ↓
4. Test Data Mapping (Deviation threshold)
   ↓
5. Visualization (Bokeh)
   ↓
6. Results Storage (Database + HTML)
```

### Configuration

Edit `config.py` to customize:
- Database location
- Data file paths
- Output directory
- Algorithm parameters
- Visualization settings

### Advanced Usage

#### Custom Application Instance

```python
from main import Application

# Create application
app = Application(db_path="my_database.db")

# Load data
app.load_data(
    training_files=["train1.csv"],
    ideal_file="ideal_funcs.csv",
    test_file="test.csv"
)

# Initialize database
app.initialize_database()

# Select ideal functions
app.select_ideal_functions()

# Map test data
app.map_test_data()

# Generate visualizations
app.visualize_results()

# Access results programmatically
for key, value in app.selected_ideal_functions.items():
    print(f"{key}: Function #{value['index']}, Max Dev: {value['max_deviation']}")

# Clean up
app.db.close()
```

#### Query Database Results

```python
from database import Database, TestDataDB

db = Database()
db.init_db()
session = db.get_session()

# Get all test data
results = session.query(TestDataDB).all()

for result in results:
    print(f"X: {result.x}, Y: {result.y}, "
          f"Function: {result.ideal_function_no}, "
          f"Deviation: {result.delta_y}")

session.close()
db.close()
```

### Performance Tips

1. **For Large Datasets**: Comment out visualization generation
2. **For Many Ideal Functions**: Use multiprocessing in selector
3. **For Multiple Runs**: Keep database and clear tables instead of recreating

### Next Steps

1. Explore the generated `visualization.html` file
2. Query the SQLite database to review results
3. Modify CSV data and rerun to see different results
4. Review the source code to understand the implementation
5. Run tests to verify functionality

### Support

For issues or questions:
1. Check README.md for detailed documentation
2. Review docstrings in source files
3. Run tests to verify installation
4. Check console error messages

---

**Happy Coding!** 🐍
