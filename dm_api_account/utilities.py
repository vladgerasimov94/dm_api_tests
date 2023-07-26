import allure
from pydantic import BaseModel
from requests import Response
from string import ascii_letters, digits
import random


def validate_request_json(json: str | BaseModel):
    with allure.step("Валидация отправляемого в request json"):
        if isinstance(json, dict):
            return json
        return json.model_dump(by_alias=True, exclude_none=True)


def validate_status_code(response: Response, status_code: int):
    with allure.step("Проверка валидации и статус кода"):
        assert response.status_code == status_code, f"Expected status code: {status_code}, got: {response.status_code}"


def random_string(begin: int = 1, end: int = 30) -> str:
    with allure.step("Генерация рандомной строки"):
        symbols = ascii_letters + digits
        string = ""
        for _ in range(random.randint(begin, end)):
            string += random.choice(symbols)
        return string
