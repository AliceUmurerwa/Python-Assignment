# Quick Reference Card

## IU CSEMDSPWP01 - Python Project Quick Start

### Installation (5 minutes)
```bash
cd "C:\Users\25078\Desktop\Python Assignment"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Run Application (2 minutes)
```bash
python generate_sample_data.py    # Generate test data
python main.py                     # Run application
# Results in: output/visualization.html and ideal_functions.db
```

### Run Tests (1 minute)
```bash
pytest tests/ -v                   # Run all tests
pytest tests/test_main.py -v      # Run specific test file
```

---

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | Run the application |
| `database.py` | SQLAlchemy models |
| `data_loader.py` | Load CSV files |
| `ideal_function_selector.py` | Least Squares algorithm |
| `test_mapper.py` | Map test data |
| `visualization.py` | Create Bokeh plots |

---

## Expected Output

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

---

## Project Structure

```
Python Assignment/
├── main.py                          # Main application
├── database.py                      # Database models
├── models.py                        # Data models
├── data_loader.py                   # CSV loaders
├── ideal_function_selector.py       # Least Squares
├── test_mapper.py                   # Test mapping
├── visualization.py                 # Bokeh plots
├── exceptions.py                    # Custom errors
├── config.py                        # Configuration
├── generate_sample_data.py          # Data generator
├── tests/
│   ├── __init__.py
│   └── test_main.py                # 30+ tests
├── requirements.txt                 # Dependencies
├── pytest.ini                       # Test config
├── README.md                        # Full documentation
├── GETTING_STARTED.md              # Quick start
├── DEVELOPMENT_GUIDE.md            # Dev guide
└── PROJECT_COMPLETION_SUMMARY.md   # This file
```

---

## Key Classes

### Application
```python
from main import Application

app = Application()
app.run(
    training_files=['train.csv'],
    ideal_file='ideal.csv',
    test_file='test.csv'
)
```

### DataLoader Hierarchy
```python
DataLoader (base class)
├── TrainingDataLoader
├── IdealFunctionLoader
└── TestDataLoader
```

### IdealFunctionSelector
```python
from ideal_function_selector import IdealFunctionSelector

selector = IdealFunctionSelector()
idx, dev, perpoint = selector.select_ideal_function(...)
results = selector.select_all_ideal_functions(...)
```

---

## Common Tasks

### Generate Sample Data
```bash
python generate_sample_data.py
```
Generates:
- `train_data_1.csv` (100 points)
- `ideal_functions.csv` (100 rows × 50 functions)
- `test_data.csv` (50 points)

### Query Database Results
```python
from database import Database, TestDataDB

db = Database()
db.init_db()
session = db.get_session()

results = session.query(TestDataDB).all()
for r in results:
    print(f"X: {r.x}, Assigned Function: {r.ideal_function_no}")

session.close()
db.close()
```

### View Visualizations
Open `output/visualization.html` in web browser

### Run Specific Test
```bash
pytest tests/test_main.py::TestIdealFunctionSelector::test_calculate_squared_deviations -v
```

---

## CSV File Formats

### Training Data (train_data_1.csv)
```
x,y1,y2,y3,y4
1.0,1.1,1.2,1.3,1.4
2.0,2.1,2.2,2.3,2.4
```

### Ideal Functions (ideal_functions.csv)
```
x,y1,y2,...,y50
1.0,0.841,0.540,...,1.234
2.0,0.909,0.416,...,1.567
```

### Test Data (test_data.csv)
```
x,y
1.0,1.1
2.0,2.1
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | `pip install -r requirements.txt` |
| File not found | `python generate_sample_data.py` |
| Database locked | Delete `ideal_functions.db` and rerun |
| Tests fail | Ensure dependencies installed and Python 3.8+ |

---

## Dependencies

- pandas 2.0.3 - Data manipulation
- numpy 1.24.3 - Numerical computing
- sqlalchemy 2.0.19 - Database ORM
- bokeh 3.3.0 - Visualization
- pytest 7.4.0 - Testing

---

## Algorithm

**Least Squares**: Select ideal function with minimum sum of squared deviations

$$SSD = \sum_{i=1}^{n} (Y_{training,i} - Y_{ideal,i})^2$$

**Test Mapping**: Assign test point if:

$$|Y_{test} - Y_{ideal}| \leq \max(deviation) \times \sqrt{2}$$

---

## Documentation Files

- **README.md**: Complete project documentation
- **GETTING_STARTED.md**: Step-by-step setup guide
- **DEVELOPMENT_GUIDE.md**: Development and extension guide
- **PROJECT_COMPLETION_SUMMARY.md**: This summary

---

## Quick Commands

```bash
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Generate data
python generate_sample_data.py

# Run app
python main.py

# Run tests
pytest tests/ -v

# Run specific test
pytest tests/test_main.py::TestTrainingData -v
```

---

## Code Example: Complete Workflow

```python
from main import Application

# Create application
app = Application(db_path="my_project.db")

# Load data
app.load_data(
    training_files=["train.csv"],
    ideal_file="ideal.csv",
    test_file="test.csv"
)

# Initialize database
app.initialize_database()

# Select ideal functions
app.select_ideal_functions()

# Map test data
app.map_test_data()

# Create visualizations
app.visualize_results()

# Access results
for key, value in app.selected_ideal_functions.items():
    print(f"{key}: Function #{value['index']}")

# Cleanup
app.db.close()
```

---

## Status: ✅ COMPLETE

All requirements implemented and tested. Ready for use!

---

**For detailed information, see README.md, GETTING_STARTED.md, or DEVELOPMENT_GUIDE.md**
