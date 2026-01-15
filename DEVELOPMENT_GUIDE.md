"""
Development Guide for the IU CSEMDSPWP01 Python Project.

This file provides guidelines for extending and maintaining the project.
"""

# =============================================================================
# PROJECT STRUCTURE AND DESIGN PATTERNS
# =============================================================================

"""
ARCHITECTURAL LAYERS:

1. DATA LAYER (data_loader.py, models.py)
   - Handles data loading and validation
   - Defines data models
   - Implements inheritance: DataLoader (base) -> specific loaders

2. DATABASE LAYER (database.py)
   - SQLAlchemy ORM models
   - Database connection management
   - CRUD operations

3. LOGIC LAYER (ideal_function_selector.py, test_mapper.py)
   - Core algorithm implementation
   - Business logic
   - Data transformations

4. PRESENTATION LAYER (visualization.py)
   - Bokeh visualization generation
   - Output formatting

5. APPLICATION LAYER (main.py)
   - Orchestration
   - Workflow management
   - Error handling

6. UTILITY LAYER (exceptions.py, config.py)
   - Custom exceptions
   - Configuration management
"""

# =============================================================================
# DESIGN PATTERNS USED
# =============================================================================

"""
1. INHERITANCE (OOP)
   Location: data_loader.py
   
   Base Class:
   class DataLoader:
       - Shared CSV loading functionality
       - Common validation logic
   
   Subclasses:
   - TrainingDataLoader
   - IdealFunctionLoader
   - TestDataLoader

2. SINGLETON-LIKE PATTERN (Database)
   Location: database.py
   
   class Database:
       - Single database connection per application instance
       - Manages engine and session factory

3. FACTORY PATTERN (Implicit)
   Location: data_loader.py
   
   Each loader creates specific data model instances
   - load_training_data() -> List[TrainingData]
   - load_ideal_functions() -> List[IdealFunction]

4. DEPENDENCY INJECTION
   Location: main.py, test_mapper.py
   
   Components receive dependencies:
   - TestDataMapper(db: Database)
   - Improves testability and modularity

5. EXCEPTION HANDLING PATTERN
   Location: exceptions.py, all modules
   
   Custom exceptions for different failure scenarios
   - Specific exception types
   - Clear error messages
   - Proper error propagation
"""

# =============================================================================
# CODE QUALITY STANDARDS
# =============================================================================

"""
1. PEP 8 COMPLIANCE
   - Lines up to ~100 characters
   - 4-space indentation
   - Two blank lines between classes
   - One blank line between methods

2. TYPE HINTS
   Example:
   def select_ideal_function(
       self,
       training_data: List[TrainingData],
       ideal_functions: List[IdealFunction],
       training_index: int,
   ) -> Tuple[int, float, List[float]]:
       ...

3. DOCUMENTATION
   - Module docstrings at file top
   - Class docstrings with purpose
   - Method docstrings with Args, Returns, Raises
   - Inline comments for complex logic

   Example:
   def calculate_squared_deviations(
       training_y: float, ideal_y: float
   ) -> float:
       '''Calculate squared deviation between a training point 
          and ideal function point.

       Args:
           training_y: Y value from training data.
           ideal_y: Y value from ideal function.

       Returns:
           Squared deviation.
       '''
       return (training_y - ideal_y) ** 2
"""

# =============================================================================
# EXTENDING THE PROJECT
# =============================================================================

"""
TO ADD A NEW FEATURE:

1. Create the logic in an appropriate module
2. Add corresponding database models if needed
3. Add exception types to exceptions.py
4. Update configuration in config.py
5. Add tests in tests/
6. Update README.md
7. Add docstrings with Args, Returns, Raises
8. Use type hints

EXAMPLE: Adding a new analysis feature

Step 1: Create module (analysis.py)
   class StatisticalAnalyzer:
       '''Performs statistical analysis on data.'''
       
       def calculate_statistics(self, data: List[float]) -> dict:
           '''Calculate mean, std, etc.'''
           ...

Step 2: Add to database (database.py)
   class AnalysisResultsDB(Base):
       '''Store analysis results.'''
       ...

Step 3: Add exception (exceptions.py)
   class AnalysisError(Exception):
       '''Exception for analysis failures.'''
       pass

Step 4: Update config (config.py)
   ANALYSIS_THRESHOLD = 0.05

Step 5: Add tests (tests/test_analysis.py)
   class TestStatisticalAnalyzer:
       def test_calculate_statistics(self):
           ...

Step 6: Integrate into main.py
   from analysis import StatisticalAnalyzer
   analyzer = StatisticalAnalyzer()
   results = analyzer.calculate_statistics(data)

Step 7: Update documentation
   README.md - Add feature description
   GETTING_STARTED.md - Add usage example
"""

# =============================================================================
# TESTING GUIDELINES
# =============================================================================

"""
TEST STRUCTURE:

Each module has corresponding tests:
- models.py -> test_main.py (TestTrainingData, TestIdealFunction, etc.)
- data_loader.py -> test_main.py (TestTrainingDataLoader, etc.)
- database.py -> test_main.py (TestDatabase, etc.)

TEST CATEGORIES:

1. UNIT TESTS - Test individual functions
   def test_calculate_squared_deviations(self):
       selector = IdealFunctionSelector()
       deviation = selector.calculate_squared_deviations(5.0, 3.0)
       assert deviation == 4.0

2. INTEGRATION TESTS - Test component interactions
   def test_database_insert_and_retrieve(self):
       db = Database(":memory:")
       db.init_db()
       # Insert and retrieve data

3. ERROR TESTS - Test exception handling
   def test_training_data_invalid_y_count(self):
       with pytest.raises(ValueError):
           TrainingData(x=1.0, y_values=[1.1, 2.2])

RUNNING TESTS:

pytest                          # Run all tests
pytest -v                       # Verbose output
pytest tests/test_main.py       # Specific file
pytest -k "test_database"       # Tests matching pattern
pytest --cov=.                  # With coverage
pytest -x                       # Stop on first failure
pytest --pdb                    # Debug on failure
"""

# =============================================================================
# COMMON MODIFICATIONS
# =============================================================================

"""
CHANGE 1: Modify the deviation threshold formula
   File: test_mapper.py, map_test_point()
   From: threshold = max_training_deviation * math.sqrt(2)
   To:   threshold = max_training_deviation * 1.5  # Increase tolerance

CHANGE 2: Add more ideal functions
   File: models.py, IdealFunction
   Add Y columns up to y100 in database.py, IdealFunctionDB
   Update config.py: IDEAL_FUNCTION_COUNT = 100

CHANGE 3: Use different algorithm for selection
   File: ideal_function_selector.py
   Replace sum_squared_deviations() with your algorithm
   Update documentation

CHANGE 4: Change database backend
   File: database.py, main.py
   From: db_url = f"sqlite:///{os.path.abspath(self.db_path)}"
   To:   db_url = "postgresql://user:password@localhost/dbname"
   Update requirements.txt with psycopg2

CHANGE 5: Add logging
   File: main.py, utils.py
   
   import logging
   logger = logging.getLogger(__name__)
   logger.info("Starting data load...")
   logger.debug(f"Loaded {len(data)} records")
   logger.error(f"Failed to load: {error}")
"""

# =============================================================================
# PERFORMANCE OPTIMIZATION
# =============================================================================

"""
OPTIMIZATION TECHNIQUES:

1. VECTORIZATION (NumPy)
   Before: sum([calculate_squared_deviations(t, i) for t, i in zip(...)])
   After:  np.sum((np.array(training) - np.array(ideal))**2)

2. BATCH PROCESSING
   Process test data in chunks instead of one at a time
   
3. CACHING
   Cache ideal function indices after selection
   
4. MULTIPROCESSING
   Parallelize ideal function selection for 4 datasets
   from multiprocessing import Pool

5. DATABASE INDEXING
   In database.py:
   x = Column(Float, nullable=False, unique=True, index=True)

6. LAZY LOADING
   Load data only when needed instead of all at once
"""

# =============================================================================
# DEBUGGING TIPS
# =============================================================================

"""
1. ENABLE DEBUG OUTPUT
   In main.py, Database.__init__:
   self.engine = create_engine(db_url, echo=True)  # SQL logging

2. PRINT STATEMENTS
   print(f"Training data loaded: {len(self.training_data_sets)}")
   print(f"Ideal functions: {len(self.ideal_functions)}")

3. USE DEBUGGER
   import pdb
   pdb.set_trace()  # Breakpoint

4. INSPECT DATABASE
   from database import Database, TestDataDB
   db = Database()
   db.init_db()
   session = db.get_session()
   records = session.query(TestDataDB).all()
   for r in records:
       print(r.__dict__)

5. TEST SMALL PARTS
   python -c "
   from data_loader import TrainingDataLoader
   loader = TrainingDataLoader()
   data, df = loader.load_training_data('train_data_1.csv')
   print(f'Loaded {len(data)} records')
   "
"""

# =============================================================================
# VERSION CONTROL
# =============================================================================

"""
GIT IGNORE (.gitignore):

__pycache__/
*.py[cod]
*.so
.Python
env/
venv/
*.db
output/
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/

COMMIT MESSAGES:
- feat: Add new feature
- fix: Bug fix
- docs: Documentation update
- test: Add tests
- refactor: Code refactoring
- perf: Performance improvement

Example:
git commit -m "feat: Add multiprocessing for ideal function selection"
git commit -m "fix: Handle edge case in test data mapping"
git commit -m "test: Add 5 new tests for database operations"
"""

# =============================================================================
# DOCUMENTATION MAINTENANCE
# =============================================================================

"""
UPDATE CHECKLIST:

□ README.md - Update if features change
□ GETTING_STARTED.md - Update if setup changes
□ Docstrings - Update when modifying functions
□ config.py - Comment new configuration options
□ Type hints - Add for all new functions
□ requirements.txt - Update with new dependencies

Example docstring update:
Before: '''Load training data.'''
After:  '''Load training data from CSV file with validation.
        
           Args:
               file_path: Path to training CSV file.
               
           Returns:
               Tuple of (list of TrainingData, DataFrame).
               
           Raises:
               DataLoadError: If file cannot be loaded.
               InvalidDataError: If validation fails.
        '''
"""

# =============================================================================
# TROUBLESHOOTING FOR DEVELOPERS
# =============================================================================

"""
ISSUE: ImportError when running code
SOLUTION: Check sys.path includes project root
          import sys; sys.path.insert(0, '.')

ISSUE: SQLAlchemy relationship errors
SOLUTION: Review Base.metadata.create_all(engine) is called

ISSUE: Pandas SettingWithCopyWarning
SOLUTION: Use .copy() when creating DataFrame subsets
          df = df[df.x > 0].copy()

ISSUE: Memory leak with large datasets
SOLUTION: Close sessions explicitly
          session.close()
          
          Or use context manager:
          with db.get_session() as session:
              # work with session

ISSUE: Visualizations not rendering
SOLUTION: Ensure output directory exists
          os.makedirs('output', exist_ok=True)
          
          Check Bokeh version compatibility
          pip install --upgrade bokeh

ISSUE: Type hint errors with mypy
SOLUTION: mypy main.py --ignore-missing-imports
"""

# =============================================================================
# CONTRIBUTING CODE
# =============================================================================

"""
BEFORE SUBMITTING:

1. Format code with PEP 8
2. Add type hints
3. Write docstrings
4. Add unit tests
5. Verify all tests pass: pytest -v
6. Update documentation
7. No hardcoded paths - use config.py
8. No print() debugging - use logging
9. Handle exceptions properly
10. Follow existing code style

REVIEW CHECKLIST:

Code Quality:
□ PEP 8 compliant
□ Type hints on all functions
□ Docstrings with Args, Returns, Raises
□ Error handling with custom exceptions

Functionality:
□ All tests pass
□ No breaking changes
□ Performance acceptable
□ Works with sample data

Documentation:
□ README updated
□ Docstrings complete
□ Type hints correct
□ Comments for complex logic

Testing:
□ Unit tests added
□ Edge cases covered
□ Error cases tested
□ Coverage maintained
"""

# =============================================================================
