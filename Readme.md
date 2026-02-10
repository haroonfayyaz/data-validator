# Data Validator

A full-stack application for validating CSV files with volume, email completeness, and age validity checks.

## Features

- **Volume Validation**: Ensures CSV files have more than 10 data rows
- **Email Completeness**: Validates that all rows have non-empty email addresses
- **Age Validity**: Checks that ages are valid integers within the range 18-100 (inclusive)

## Prerequisites

- Python 3.13
- Node.js 22+
- pnpm (for frontend)
- Docker & Docker Compose (optional, for containerized deployment)

## Setup

### Backend

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

### Frontend

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
pnpm install
```

3. Create `.env` file (copy from `example.env`):
```bash
cp example.env .env
```

4. Update `VITE_API_BASE_URL` in `.env` if needed (default: `http://localhost:8000`)

## Running the Application

### Development Mode

**Backend:**
```bash
python run_backend.py
```
The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

**Frontend:**
```bash
cd frontend
pnpm run dev
```
The frontend will be available at `http://localhost:3000`

### Docker Compose

Build and run both services:
```bash
docker-compose up --build
```

Backend: `http://localhost:8000`
Frontend: `http://localhost:3000`

To run in detached mode:
```bash
docker-compose up -d
```

To stop:
```bash
docker-compose down
```

## Frontend-Backend Communication

The frontend and backend communicate via REST API using HTTP requests.

### Architecture

- **Frontend**: React application using Axios for HTTP requests
- **Backend**: FastAPI REST API server
- **Communication**: JSON over HTTP with multipart/form-data for file uploads

### API Client Setup

The frontend uses a centralized Axios instance configured in `frontend/src/services/api.ts`:

- **Base URL**: Configured via `VITE_API_BASE_URL` environment variable
- **Default**: `http://localhost:8000` (development)
- **Production**: Set via environment variable during build

### CORS Configuration

The backend is configured with CORS middleware to allow requests from the frontend:

- **Development**: Allows `http://localhost:3000` and `http://localhost`
- **Headers**: All headers and methods are allowed

### Request Flow

1. User uploads CSV file through the React frontend
2. Frontend creates FormData and sends POST request to `/validate` endpoint
3. Backend receives file, validates using Pandas, and returns JSON response
4. Frontend displays validation results (success banner or error table)

### Error Handling

The frontend includes comprehensive error handling for:
- Network connection issues
- Server errors (500, 502, etc.)
- Request timeouts
- Invalid file formats
- User-friendly error messages displayed in the UI

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

## Sample CSV Files

The `data/` directory contains sample CSV files for testing:

- `test_data_clean.csv` - Valid data (passes all checks)
- `test_data_dirty.csv` - Contains various validation errors

## Testing

Run tests from the project root:

```bash
pytest
```

Or with verbose output:

```bash
pytest -v
```
