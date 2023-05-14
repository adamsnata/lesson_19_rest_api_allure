import pytest
import requests
from pytest_voluptuous import S
from requests import Response

from schemas.reqres import list_users_schema


def test_get_users_page_number(reqres):
    """Когда запросили вторую страницу, убеждаемся что вернулась вторая страница."""

    response: Response = reqres.get("/users?page=2")

    assert response.status_code == 200
    assert response.json()["page"] == 2


def test_get_users_users_on_page(reqres):
    """Проверяем дефолтное количество пользователей на странице и что вернулось столько же пользователей."""
    response: Response = reqres.get("/users?page=2")
    per_page = response.json()["per_page"]
    data_len = len(response.json()["data"])

    assert data_len == per_page == 6


def test_get_users_validate_schema():
    """Валидируем схему ответа. Передаем query-params в requests правильно."""
    url = "https://reqres.in/api/users"

    response: Response = requests.get(url, params={"page": 2})

    assert S(list_users_schema) == response.json()


@pytest.mark.parametrize("path_part", ["users", "cutomers", "products"])
def test_get_path_is_200(path_part):
    """Как параметризовать API тест с множеством путей, когда надо проверить только 200 коды для каждого урла."""
    url = f"https://reqres.in/api/{path_part}"

    response: Response = requests.get(url)

    assert response.status_code == 200
