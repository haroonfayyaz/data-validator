from typing import List, Dict, Any, Optional
import pandas as pd
from backend.config import MIN_ROWS, MIN_AGE, MAX_AGE

REQUIRED_COLUMNS = ["id", "email", "age"]


def validate_required_columns(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """
    Check if all required columns are present in the CSV.
    Returns error dict if any column is missing, None if all present.
    """
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        columns_str = ", ".join(missing_columns)
        return {
            "row_index": None,
            "id": None,
            "column": "schema",
            "error_message": f"Required column(s) missing: {columns_str}"
        }
    return None


def validate_volume(df: pd.DataFrame) -> Optional[Dict[str, Any]]:
    """
    Check if CSV has more than 10 data rows.
    Returns error dict if validation fails, None if passes.
    Row 0 is header, so we need more than 10 data rows (row_count > 10).
    """
    row_count = len(df)
    if row_count <= MIN_ROWS:
        return {
            "row_index": None,
            "id": None,
            "column": "volume",
            "error_message": f"File must contain more than {MIN_ROWS} data rows. Found {row_count} row(s)."
        }
    return None


def validate_email_completeness(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Check email column for empty or null values.
    Returns list of error objects for each row with missing email.
    Assumes required columns have already been validated.
    """
    errors = []

    for idx in range(len(df)):
        email_value = df.iloc[idx]["email"]
        if pd.isna(email_value) or (isinstance(email_value, str) and email_value.strip() == ""):
            row_index = idx + 1
            id_value = df.iloc[idx]["id"]
            errors.append({
                "row_index": row_index,
                "id": int(id_value) if pd.notna(id_value) else None,
                "column": "email",
                "error_message": "Email is empty or null"
            })

    return errors


def validate_age(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Check age column for valid integers between 18-100.
    Distinguishes between invalid format and out of range errors.
    Returns list of error objects for each invalid age.
    Assumes required columns have already been validated.
    """
    errors = []

    for idx in range(len(df)):
        age_value = df.iloc[idx]["age"]
        row_index = idx + 1
        id_value = df.iloc[idx]["id"]

        # Check if age is missing/null
        if pd.isna(age_value):
            errors.append({
                "row_index": row_index,
                "id": int(id_value) if pd.notna(id_value) else None,
                "column": "age",
                "error_message": "Age is empty or null"
            })
            continue

        # Try to parse as integer
        try:
            # Convert to string, strip whitespace, then try to convert to float then int
            age_str = str(age_value).strip()
            age_int = int(float(age_str))

            # Check if within valid range
            if age_int < MIN_AGE or age_int > MAX_AGE:
                errors.append({
                    "row_index": row_index,
                    "id": int(id_value) if pd.notna(id_value) else None,
                    "column": "age",
                    "error_message": f"Age {age_int} is outside the allowed range ({MIN_AGE}-{MAX_AGE})"
                })
        except (ValueError, TypeError):
            # Invalid format
            errors.append({
                "row_index": row_index,
                "id": int(id_value) if pd.notna(id_value) else None,
                "column": "age",
                "error_message": f"Invalid age format: '{age_value}'"
            })

    return errors
