import pytest
from fastapi.testclient import TestClient
from backend.main import app
import io

client = TestClient(app)


class TestValidateEndpoint:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Data Validator API"}

    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_validate_valid_csv(self):
        csv_data = "id,email,age\n"
        for i in range(1, 12):
            csv_data += f"{i},test{i}@xovate.com,{25+i}\n"

        response = client.post(
            "/validate",
            files={"file": ("test.csv", io.BytesIO(csv_data.encode()), "text/csv")}
        )
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "errors" in data
        assert data["status"] == "pass"
        assert len(data["errors"]) == 0

    def test_validate_invalid_file_type(self):
        response = client.post(
            "/validate",
            files={"file": ("test.txt", io.BytesIO(b"not a csv"), "text/plain")}
        )
        assert response.status_code == 400
        assert "CSV file" in response.json()["detail"]

    def test_validate_volume_failure(self):
        csv_data = "id,email,age\n"
        for i in range(1, 6):
            csv_data += f"{i},test{i}@xovate.com,30\n"

        response = client.post(
            "/validate",
            files={"file": ("test.csv", io.BytesIO(csv_data.encode()), "text/csv")}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "fail"
        assert len(data["errors"]) == 1
        assert data["errors"][0]["column"] == "volume"
        assert data["errors"][0]["row_index"] is None
        assert data["errors"][0]["id"] is None

    def test_validate_email_missing(self):
        csv_data = "id,email,age\n"
        for i in range(1, 12):
            email = f"test{i}@xovate.com" if i % 2 == 0 else ""
            csv_data += f"{i},{email},30\n"

        response = client.post(
            "/validate",
            files={"file": ("test.csv", io.BytesIO(csv_data.encode()), "text/csv")}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "fail"
        email_errors = [e for e in data["errors"] if e["column"] == "email"]
        assert len(email_errors) > 0
        assert all(e["row_index"] is not None for e in email_errors)

    def test_validate_age_invalid_format(self):
        csv_data = "id,email,age\n"
        csv_data += "1,test1@xovate.com,30\n"
        csv_data += "2,test2@xovate.com,30yrs\n"
        csv_data += "3,test3@xovate.com,25\n"
        for i in range(4, 12):
            csv_data += f"{i},test{i}@xovate.com,30\n"

        response = client.post(
            "/validate",
            files={"file": ("test.csv", io.BytesIO(csv_data.encode()), "text/csv")}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "fail"
        age_errors = [e for e in data["errors"] if e["column"] == "age"]
        assert len(age_errors) == 1
        assert "Invalid age format" in age_errors[0]["error_message"]

    def test_validate_age_out_of_range(self):
        csv_data = "id,email,age\n"
        csv_data += "1,test1@xovate.com,30\n"
        csv_data += "2,test2@xovate.com,17\n"
        csv_data += "3,test3@xovate.com,101\n"
        for i in range(4, 12):
            csv_data += f"{i},test{i}@xovate.com,30\n"

        response = client.post(
            "/validate",
            files={"file": ("test.csv", io.BytesIO(csv_data.encode()), "text/csv")}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "fail"
        age_errors = [e for e in data["errors"] if e["column"] == "age"]
        assert len(age_errors) == 2
        assert all("outside the allowed range" in e["error_message"] for e in age_errors)

    def test_validate_multiple_errors_per_row(self):
        csv_data = "id,email,age\n"
        csv_data += "1,test1@xovate.com,30\n"
        csv_data += "2,,17\n"  # Missing email and invalid age
        for i in range(3, 12):
            csv_data += f"{i},test{i}@xovate.com,30\n"

        response = client.post(
            "/validate",
            files={"file": ("test.csv", io.BytesIO(csv_data.encode()), "text/csv")}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "fail"
        row_2_errors = [e for e in data["errors"] if e["row_index"] == 2]
        assert len(row_2_errors) == 2
        assert any(e["column"] == "email" for e in row_2_errors)
        assert any(e["column"] == "age" for e in row_2_errors)

    def test_validate_missing_required_column(self):
        csv_data = "id,email\n"  # Missing age column
        for i in range(1, 12):
            csv_data += f"{i},test{i}@xovate.com\n"

        response = client.post(
            "/validate",
            files={"file": ("test.csv", io.BytesIO(csv_data.encode()), "text/csv")}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "fail"
        assert len(data["errors"]) == 1
        assert data["errors"][0]["column"] == "schema"
        assert data["errors"][0]["row_index"] is None
        assert data["errors"][0]["id"] is None
        assert "age" in data["errors"][0]["error_message"].lower()

    def test_validate_missing_multiple_columns(self):
        csv_data = "email\n"  # Missing id and age columns
        for i in range(1, 12):
            csv_data += f"test{i}@xovate.com\n"

        response = client.post(
            "/validate",
            files={"file": ("test.csv", io.BytesIO(csv_data.encode()), "text/csv")}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "fail"
        assert len(data["errors"]) == 1
        assert data["errors"][0]["column"] == "schema"
        assert "id" in data["errors"][0]["error_message"].lower()
        assert "age" in data["errors"][0]["error_message"].lower()

    def test_validate_missing_columns_skips_all_checks(self):
        csv_data = "id,email\n"  # Missing age column
        csv_data += "1,test1@xovate.com\n"
        csv_data += "2,test2@xovate.com\n"
        # Even though volume check would fail, missing column check should stop it

        response = client.post(
            "/validate",
            files={"file": ("test.csv", io.BytesIO(csv_data.encode()), "text/csv")}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "fail"
        assert len(data["errors"]) == 1
        assert data["errors"][0]["column"] == "schema"

    def test_validate_volume_failure_skips_other_checks(self):
        csv_data = "id,email,age\n"
        csv_data += "1,,invalid\n"  # Would fail email and age, but volume check should stop it
        csv_data += "2,,invalid\n"
        csv_data += "3,,invalid\n"

        response = client.post(
            "/validate",
            files={"file": ("test.csv", io.BytesIO(csv_data.encode()), "text/csv")}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "fail"
        assert len(data["errors"]) == 1
        assert data["errors"][0]["column"] == "volume"
