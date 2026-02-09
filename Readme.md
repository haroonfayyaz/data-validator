# Data Validator

A full-stack application for validating CSV files with volume, email completeness, and age validity checks.

## Features

- **Volume Validation**: Ensures CSV files have more than 10 data rows (at least 11 rows)
- **Email Completeness**: Validates that all rows have non-empty email addresses
- **Age Validity**: Checks that ages are valid integers within the range 18-100 (inclusive)

## Project Structure

```
data-validator/
├── backend/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration constants
│   ├── validators.py        # Validation functions
│   ├── routes.py            # API route handlers
│   ├── requirements.txt     # Python dependencies
│   └── tests/               # Test suite
│       ├── __init__.py
│       ├── test_validators.py
│       └── test_routes.py
├── data/                     # Sample CSV files for testing
├── run_backend.py           # Backend server runner script
└── README.md
```

## Prerequisites

- Python 3.13+
- Node.js 22+ (for frontend, coming soon)
- Docker & Docker Compose (optional, for containerized deployment)

## Backend Setup

### Installation

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### Running the Backend

You can run the backend server in several ways:

**Option 1: Using the run script (from project root)**
```bash
python run_backend.py
```

**Option 2: Using uvicorn directly (from project root)**
```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Option 3: Running as a module (from project root)**
```bash
python -m backend.main
```

The API will be available at `http://localhost:8000`

### API Endpoints

- `GET /` - API information
- `GET /health` - Health check endpoint
- `POST /validate` - Validate CSV file upload

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Validate Endpoint

**POST /validate**

Upload a CSV file for validation.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (CSV file)

**Response Format:**
```json
{
  "status": "pass" | "fail",
  "errors": [
    {
      "row_index": <int or null>,
      "id": <int or null>,
      "column": "<column name>",
      "error_message": "<description>"
    }
  ]
}
```

**Example - Valid CSV (pass):**
```json
{
  "status": "pass",
  "errors": []
}
```

**Example - Volume Check Failure:**
```json
{
  "status": "fail",
  "errors": [
    {
      "row_index": null,
      "id": null,
      "column": "volume",
      "error_message": "File must contain more than 10 data rows. Found 5 row(s)."
    }
  ]
}
```

**Example - Row-level Errors:**
```json
{
  "status": "fail",
  "errors": [
    {
      "row_index": 3,
      "id": 3,
      "column": "email",
      "error_message": "Email is empty or null"
    },
    {
      "row_index": 4,
      "id": 4,
      "column": "age",
      "error_message": "Age 17 is outside the allowed range (18-100)"
    },
    {
      "row_index": 5,
      "id": 5,
      "column": "age",
      "error_message": "Invalid age format: '30yrs'"
    }
  ]
}
```

### Validation Rules

#### Required Columns
The validator expects the following columns in the CSV:
- `id` - Row identifier (used for error reporting)
- `email` - Email address
- `age` - Age value

**Missing Column Handling:**
- If `id` column is missing: `id` field in error responses will be `null`
- If `email` column is missing: All rows will receive an error indicating the column is missing
- If `age` column is missing: All rows will receive an error indicating the column is missing

#### Check A: Volume Check (Global)
- **Rule**: The file must contain **more than 10 data rows** (i.e., at least 11 rows)
- **Row numbering**: Row 0 is the header row, first data row is row 1
- **Failure behavior**: If this check fails, only one global error is returned and all other validation checks are skipped
- **Error format**: `row_index: null, id: null, column: "volume"`

#### Check B: Email Completeness
- **Rule**: The email column must not be empty or null
- **Failure**: For each row where email is missing, a separate error record is generated
- **Error includes**: `row_index` (starting from 1) and `id` (from CSV id column)

#### Check C: Age Validity
- **Rule**: The age column must contain a valid integer between 18 and 100 (inclusive)
- **Failure types**:
  1. **Invalid format**: Non-numeric values (e.g., "30yrs", "unknown", "N/A", "approx 24", "TBA")
     - Error message: "Invalid age format: '<value>'"
  2. **Out of range**: Integers outside 18-100 (e.g., 17, 12, 101)
     - Error message: "Age <value> is outside the allowed range (18-100)"
- **Error includes**: `row_index` (starting from 1) and `id` (from CSV id column)

#### Multiple Errors Per Row
A single row may fail multiple checks (e.g., missing email and invalid age). Each failure produces a separate error object with the same `id` and `row_index`.

## Testing

### Running Tests

From the project root:

```bash
# Run all tests
pytest backend/tests/

# Run with verbose output
pytest backend/tests/ -v

# Run specific test file
pytest backend/tests/test_validators.py

# Run specific test class
pytest backend/tests/test_validators.py::TestValidateVolume

# Run with coverage
pytest backend/tests/ --cov=backend --cov-report=html
```

### Test Coverage

The test suite includes:
- Unit tests for all validation functions
- Integration tests for API endpoints
- Edge cases and error handling

## Sample CSV Files

The `data/` directory contains sample CSV files:
- `test_data_clean.csv` - Valid data (passes all checks)
- `test_data_dirty.csv` - Contains various validation errors
- `test_data_sample.csv` - Small sample file
- `test_data_missing_age.csv` - Missing age values

## Development

### Code Structure

The backend follows a modular architecture:

- **config.py**: Centralized configuration constants
- **validators.py**: Pure validation functions (easily testable)
- **routes.py**: API route handlers and business logic
- **main.py**: FastAPI app setup and endpoint definitions

### Adding New Validators

1. Add validation function to `backend/validators.py`
2. Import and call it in `backend/routes.py`
3. Add it to the response in the `validate_csv` function
4. Write tests in `backend/tests/test_validators.py`

## License

MIT
