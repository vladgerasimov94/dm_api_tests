from pydantic import BaseModel
from requests import Response


def validate_request_json(json: str | BaseModel):
    if isinstance(json, dict):
        return json
    return json.model_dump(by_alias=True, exclude_none=True)


def validate_status_code(response: Response, status_code: int):
    assert response.status_code == status_code, f"Expected status code: {status_code}, got: {response.status_code}"
