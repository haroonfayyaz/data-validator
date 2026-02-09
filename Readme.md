# Data Validator

A full-stack application for validating CSV files with volume, email completeness, and age validity checks.

## Features

- **Volume Validation**: Ensures CSV files have more than 10 data rows
- **Email Completeness**: Validates that all rows have non-empty email addresses
- **Age Validity**: Checks that ages are valid integers within the range 18-100 (inclusive)

## Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

## Running the Backend

```bash
python run_backend.py
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## API Endpoint

**POST /validate**

Upload a CSV file for validation.

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

## Validation Rules

**Required Columns:** `id`, `email`, `age`

**Missing Column Handling:**
If any required column (`id`, `email`, or `age`) is missing from the CSV, a single global error is returned and all validation checks are skipped. This prevents processing invalid data structures and provides clear feedback about schema issues.

**Reasoning:** Missing required columns indicate a fundamental schema problem that makes row-level validation meaningless. Returning a single error is more efficient and clearer than generating errors for each row, and it prevents confusion about which validation rules apply when the data structure is incorrect.

1. **Required Columns Check**: All required columns must be present
   - If fails, returns single global error and skips all other checks

2. **Volume Check**: File must contain more than 10 data rows
   - If fails, returns single global error and skips other checks

3. **Email Completeness**: Email column must not be empty or null
   - Returns individual error for each missing email

4. **Age Validity**: Age must be valid integer between 18-100
   - Invalid format: "Invalid age format: '<value>'"
   - Out of range: "Age <value> is outside the allowed range (18-100)"

## Testing

Run tests from the project root:

```bash
pytest
```

Or with verbose output:

```bash
pytest -v
```
