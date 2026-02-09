from fastapi import UploadFile, File, HTTPException
from typing import Dict, Any, List
import pandas as pd
import io
from backend.validators import validate_volume, validate_email_completeness, validate_age


async def validate_csv(file: UploadFile) -> Dict[str, Any]:
    """
    Validate CSV file according to requirements:
    - Volume check: must have more than 10 data rows
    - Email completeness: all emails must be non-empty
    - Age validity: ages must be integers between 18-100

    Returns response in format:
    {
        "status": "pass" or "fail",
        "errors": [
            {
                "row_index": <int or null>,
                "id": <int or null>,
                "column": "<column name>",
                "error_message": "<description>"
            }
        ]
    }
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        errors: List[Dict[str, Any]] = []

        # Check A: Volume Check (Global)
        # If this fails, return single error and skip all other checks
        volume_error = validate_volume(df)
        if volume_error:
            return {
                "status": "fail",
                "errors": [volume_error]
            }

        # Volume check passed, proceed with row-level checks

        # Check B: Email Completeness
        email_errors = validate_email_completeness(df)
        errors.extend(email_errors)

        # Check C: Age Validity
        age_errors = validate_age(df)
        errors.extend(age_errors)

        # Determine status
        status = "pass" if len(errors) == 0 else "fail"

        return {
            "status": status,
            "errors": errors
        }

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
