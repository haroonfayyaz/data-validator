import pytest
import pandas as pd
from backend.validators import validate_required_columns, validate_volume, validate_email_completeness, validate_age
from backend.config import MIN_ROWS, MIN_AGE, MAX_AGE


class TestValidateRequiredColumns:
    def test_all_columns_present(self):
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "email": ["test1@xovate.com", "test2@xovate.com", "test3@xovate.com"],
            "age": [25, 30, 35]
        })
        result = validate_required_columns(df)
        assert result is None

    def test_missing_email_column(self):
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "age": [25, 30, 35]
        })
        result = validate_required_columns(df)
        assert result is not None
        assert result["row_index"] is None
        assert result["id"] is None
        assert result["column"] == "schema"
        assert "email" in result["error_message"].lower()

    def test_missing_age_column(self):
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "email": ["test1@xovate.com", "test2@xovate.com", "test3@xovate.com"]
        })
        result = validate_required_columns(df)
        assert result is not None
        assert result["column"] == "schema"
        assert "age" in result["error_message"].lower()

    def test_missing_id_column(self):
        df = pd.DataFrame({
            "email": ["test1@xovate.com", "test2@xovate.com", "test3@xovate.com"],
            "age": [25, 30, 35]
        })
        result = validate_required_columns(df)
        assert result is not None
        assert result["column"] == "schema"
        assert "id" in result["error_message"].lower()

    def test_multiple_missing_columns(self):
        df = pd.DataFrame({
            "email": ["test1@xovate.com", "test2@xovate.com", "test3@xovate.com"]
        })
        result = validate_required_columns(df)
        assert result is not None
        assert result["column"] == "schema"
        assert "id" in result["error_message"].lower()
        assert "age" in result["error_message"].lower()


class TestValidateVolume:
    def test_valid_volume_exactly_11_rows(self):
        df = pd.DataFrame({"id": range(1, 12), "email": [f"test{i}@xovate.com" for i in range(11)], "age": [25] * 11})
        result = validate_volume(df)
        assert result is None

    def test_valid_volume_more_than_11_rows(self):
        df = pd.DataFrame({"id": range(1, 21), "email": [f"test{i}@xovate.com" for i in range(20)], "age": [25] * 20})
        result = validate_volume(df)
        assert result is None

    def test_invalid_volume_exactly_10_rows(self):
        df = pd.DataFrame({"id": range(1, 11), "email": [f"test{i}@xovate.com" for i in range(10)], "age": [25] * 10})
        result = validate_volume(df)
        assert result is not None
        assert result["row_index"] is None
        assert result["id"] is None
        assert result["column"] == "volume"
        assert "more than 10" in result["error_message"].lower()

    def test_invalid_volume_less_than_10_rows(self):
        df = pd.DataFrame({"id": range(1, 6), "email": [f"test{i}@xovate.com" for i in range(5)], "age": [25] * 5})
        result = validate_volume(df)
        assert result is not None
        assert result["row_index"] is None
        assert result["id"] is None

    def test_invalid_volume_empty_dataframe(self):
        df = pd.DataFrame()
        result = validate_volume(df)
        assert result is not None
        assert result["row_index"] is None
        assert result["id"] is None


class TestValidateEmailCompleteness:
    def test_all_emails_present(self):
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "email": ["test1@xovate.com", "test2@xovate.com", "test3@xovate.com"],
            "age": [25, 30, 35]
        })
        result = validate_email_completeness(df)
        assert len(result) == 0

    def test_missing_emails_none(self):
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "email": ["test1@xovate.com", None, "test3@xovate.com"],
            "age": [25, 30, 35]
        })
        result = validate_email_completeness(df)
        assert len(result) == 1
        assert result[0]["row_index"] == 2
        assert result[0]["id"] == 2
        assert result[0]["column"] == "email"
        assert "empty or null" in result[0]["error_message"].lower()

    def test_empty_string_emails(self):
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "email": ["test1@xovate.com", "", "test3@xovate.com"],
            "age": [25, 30, 35]
        })
        result = validate_email_completeness(df)
        assert len(result) == 1
        assert result[0]["row_index"] == 2

    def test_whitespace_only_emails(self):
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "email": ["test1@xovate.com", "   ", "test3@xovate.com"],
            "age": [25, 30, 35]
        })
        result = validate_email_completeness(df)
        assert len(result) == 1
        assert result[0]["row_index"] == 2

    def test_multiple_missing_emails(self):
        df = pd.DataFrame({
            "id": [1, 2, 3, 4],
            "email": ["test1@xovate.com", None, "", "test4@xovate.com"],
            "age": [25, 30, 35, 40]
        })
        result = validate_email_completeness(df)
        assert len(result) == 2
        assert result[0]["row_index"] == 2
        assert result[1]["row_index"] == 3

    def test_id_column_missing_handles_none_id(self):
        # Note: This test assumes id column exists but has None values
        # If id column is completely missing, it's handled by validate_required_columns
        df = pd.DataFrame({
            "id": [1, None, 3],
            "email": ["test1@xovate.com", None, "test3@xovate.com"],
            "age": [25, 30, 35]
        })
        result = validate_email_completeness(df)
        assert len(result) == 1
        assert result[0]["id"] is None
        assert result[0]["row_index"] == 2


class TestValidateAge:
    def test_all_ages_valid(self):
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "email": ["test1@xovate.com", "test2@xovate.com", "test3@xovate.com"],
            "age": [25, 30, 45]
        })
        result = validate_age(df)
        assert len(result) == 0

    def test_age_at_minimum_boundary(self):
        df = pd.DataFrame({
            "id": [1, 2],
            "email": ["test1@xovate.com", "test2@xovate.com"],
            "age": [MIN_AGE, MIN_AGE + 1]
        })
        result = validate_age(df)
        assert len(result) == 0

    def test_age_at_maximum_boundary(self):
        df = pd.DataFrame({
            "id": [1, 2],
            "email": ["test1@xovate.com", "test2@xovate.com"],
            "age": [MAX_AGE, MAX_AGE - 1]
        })
        result = validate_age(df)
        assert len(result) == 0

    def test_age_too_young(self):
        df = pd.DataFrame({
            "id": [1, 2],
            "email": ["test1@xovate.com", "test2@xovate.com"],
            "age": [25, MIN_AGE - 1]
        })
        result = validate_age(df)
        assert len(result) == 1
        assert result[0]["row_index"] == 2
        assert result[0]["id"] == 2
        assert result[0]["column"] == "age"
        assert "outside the allowed range" in result[0]["error_message"]

    def test_age_too_old(self):
        df = pd.DataFrame({
            "id": [1, 2],
            "email": ["test1@xovate.com", "test2@xovate.com"],
            "age": [25, MAX_AGE + 1]
        })
        result = validate_age(df)
        assert len(result) == 1
        assert "outside the allowed range" in result[0]["error_message"]

    def test_missing_age(self):
        df = pd.DataFrame({
            "id": [1, 2],
            "email": ["test1@xovate.com", "test2@xovate.com"],
            "age": [25, None]
        })
        result = validate_age(df)
        assert len(result) == 1
        assert result[0]["row_index"] == 2
        assert "empty or null" in result[0]["error_message"].lower()

    def test_invalid_age_format_string(self):
        df = pd.DataFrame({
            "id": [1, 2],
            "email": ["test1@xovate.com", "test2@xovate.com"],
            "age": [25, "30yrs"]
        })
        result = validate_age(df)
        assert len(result) == 1
        assert result[0]["column"] == "age"
        assert "Invalid age format" in result[0]["error_message"]

    def test_invalid_age_format_na(self):
        df = pd.DataFrame({
            "id": [1, 2],
            "email": ["test1@xovate.com", "test2@xovate.com"],
            "age": [25, "N/A"]
        })
        result = validate_age(df)
        assert len(result) == 1
        assert "Invalid age format" in result[0]["error_message"]

    def test_invalid_age_format_unknown(self):
        df = pd.DataFrame({
            "id": [1, 2],
            "email": ["test1@xovate.com", "test2@xovate.com"],
            "age": [25, "unknown"]
        })
        result = validate_age(df)
        assert len(result) == 1
        assert "Invalid age format" in result[0]["error_message"]

    def test_invalid_age_format_approx(self):
        df = pd.DataFrame({
            "id": [1, 2],
            "email": ["test1@xovate.com", "test2@xovate.com"],
            "age": [25, "approx 24"]
        })
        result = validate_age(df)
        assert len(result) == 1
        assert "Invalid age format" in result[0]["error_message"]

    def test_age_as_float(self):
        df = pd.DataFrame({
            "id": [1, 2],
            "email": ["test1@xovate.com", "test2@xovate.com"],
            "age": [25.0, 30.5]
        })
        result = validate_age(df)
        assert len(result) == 0


    def test_multiple_invalid_ages(self):
        df = pd.DataFrame({
            "id": [1, 2, 3, 4],
            "email": ["test1@xovate.com", "test2@xovate.com", "test3@xovate.com", "test4@xovate.com"],
            "age": [25, 17, "invalid", None]
        })
        result = validate_age(df)
        assert len(result) == 3
        assert result[0]["row_index"] == 2
        assert "outside the allowed range" in result[0]["error_message"]
        assert result[1]["row_index"] == 3
        assert "Invalid age format" in result[1]["error_message"]
        assert result[2]["row_index"] == 4
        assert "empty or null" in result[2]["error_message"].lower()
