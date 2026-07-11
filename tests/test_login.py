import allure
import pytest
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

        response = login_courier(login, password)

        
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

        response = login_courier(login, "wrong_password")

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

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

        response = login_courier(payload.get("login"), payload.get("password"))

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

        delete_courier(login, password)


