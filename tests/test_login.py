import allure
import pytest
import requests
from constants import Urls
from helpers.helpers import generate_random_string
from api.courier_api import register_new_courier_and_return_login_password, login_courier, delete_courier_by_id


@allure.feature('Логин курьера')
class TestLogin:

    @allure.title('Логин с валидными данными')
    @allure.story('Позитивный сценарий')
    def test_login_success(self, delete_courier):
        login, password, first_name = register_new_courier_and_return_login_password()
        assert login is not None, "Курьер не создан"

        payload = {
            "login": login,
            "password": password
        }

        response = requests.post(
            f"{Urls.BASE_URL}{Urls.LOGIN_URL}",
            data=payload
        )

        assert response.status_code == 200
        assert "id" in response.json()
        assert response.json()["id"] is not None

        delete_courier(login, password)

    @allure.title('Логин с неверным паролем')
    @allure.story('Негативный сценарий')
    def test_login_invalid_password(self, delete_courier):
        login, password, first_name = register_new_courier_and_return_login_password()
        assert login is not None, "Курьер не создан"

        payload = {
            "login": login,
            "password": "wrong_password"
        }

        response = requests.post(
            f"{Urls.BASE_URL}{Urls.LOGIN_URL}",
            data=payload
        )

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text

        delete_courier(login, password)

    @allure.title('Логин без обязательных полей')
    @allure.story('Негативный сценарий')
    @pytest.mark.parametrize('field_to_remove', [
        'login'
    ])
    def test_login_missing_field(self, field_to_remove, delete_courier):
        login, password, first_name = register_new_courier_and_return_login_password()
        assert login is not None, "Курьер не создан"

        payload = {
            "login": login,
            "password": password
        }
        del payload[field_to_remove]

        response = requests.post(
            f"{Urls.BASE_URL}{Urls.LOGIN_URL}",
            data=payload
        )

        assert response.status_code == 400
        assert "Недостаточно данных" in response.text

        delete_courier(login, password)


