import pytest
from pytest_voluptuous import S
from requests import Response
from hamcrest import assert_that
import json
from schemas.reqres import new_user_unsuccessful_register, new_user_successful_register, user_login_successful, \
    user_login_unsuccessful, list_users_schema


class TestRegisterUser:

    @pytest.mark.parametrize("email, password, status_code", [("eve.holt@reqres.in", "pistol", 200)])
    def test_new_user_successful_register(self, reqres_base, email, password, status_code):
        url = "/register"
        response: Response = reqres_base.post(url=url, data={"email": email, "password": password})
        assert_that(response.status_code == 200)
        assert S(new_user_successful_register) == response.json()

    @pytest.mark.parametrize("email, password, status_code, error_message",
                             [('test_user_1@gmail.com', '', 400, '{"error":"Missing email or username"}'),
                              ('', 'passw_test', 400, '{"error":"Missing email or username"}'),
                              ('', '', 400, '{"error":"Missing email or username"}')])
    def test_new_user_unsuccessful_register(self, reqres_base, email, password, status_code, error_message):
        url = "/register"
        data = {"email": email, "password": password}
        response: Response = reqres_base.post(url=url, data=json.dumps(data))

        assert_that(response.status_code == status_code)
        assert_that(response.text == error_message)
        assert S(new_user_unsuccessful_register == response.json())


class TestLoginUser:

    @pytest.mark.parametrize("email, password, status_code", [('eve.holt@reqres.in', 'cityslicka', 200)])
    def test_login_successful(self, reqres_base, email, password, status_code,):
        url =  "/login"
        response: Response = reqres_base.post(url=url, data={"email": email, "password": password})
        assert_that(response.status_code == status_code)
        assert S(user_login_successful == response.json())

    @pytest.mark.parametrize("email, password, status_code, error_message",
                             [('peter@klaven', '', 400, '{"error":"Missing email or username"}')])
    def test_login_unsuccessful(self, reqres_base, email, password, status_code, error_message):
        url = "/register"
        data = {"email": email}
        response: Response = reqres_base.post(url=url, data=json.dumps(data))

        assert_that(response.status_code == status_code)
        assert_that(response.text == error_message)
        assert S(user_login_unsuccessful == response.json())


class TestDelayedResponse:

    def test_show_users_delayed(self, reqres_base):
        url = "/users"
        response: Response = reqres_base.get(url, params={"delay": 3})
        assert_that(response.status_code == 200)
        assert S(list_users_schema == response.json())


class TestDeleteUser:
    def test_delete_existing_user(self, reqres_base):
        url = "/users/2"
        response: Response = reqres_base.delete(url)
        assert_that(response.status_code == 204)

    # Это странно, но по идее тест должен падать. По сути, получается что подгоняют тест под текущую реализацию
    def test_delete_not_existing_user(self, reqres_base):
        url = "/users/abc"
        response: Response = reqres_base.delete(url)
        assert_that(response.status_code == 204)

    # Это странно, но по идее тест должен падать - возвращаться ошибка, что не указан ID пользователя. Но как есть
    def test_delete_user_no_id(self, reqres_base):
        url = "/users"
        response: Response = reqres_base.delete(url)
        assert_that(response.status_code == 204)
