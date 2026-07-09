import allure
import pytest
import requests
from constants import Urls
from helpers.helpers import generate_random_string, register_new_courier_and_return_login_password


#Создать курьера
@allure.feature('Создание курьера')
class TestCourier:

    @allure.title('Создание курьера с валидными данными')
    @allure.story('Позитивный сценарий')
    def test_create_courier_success(self, delete_courier):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(
            f"{Urls.BASE_URL}{Urls.COURIER_URL}",
            data=payload
        )

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        delete_courier(login, password)

    @allure.title('Создание курьера без обязательных полей')
    @allure.story('Негативный сценарий')
    @pytest.mark.parametrize('field_to_remove', [
        'login',
        'password'
    ])
    def test_create_courier_missing_field(self, field_to_remove):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        del payload[field_to_remove]

        response = requests.post(
            f"{Urls.BASE_URL}{Urls.COURIER_URL}",
            data=payload
        )

        assert response.status_code == 400
        assert "Недостаточно данных" in response.text

    @allure.title('Создание курьера с уже существующим логином')
    @allure.story('Негативный сценарий')
    def test_create_courier_duplicate_login(self, delete_courier):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }


        response1 = requests.post(
            f"{Urls.BASE_URL}{Urls.COURIER_URL}",
            data=payload
        )
        assert response1.status_code == 201


        response2 = requests.post(
            f"{Urls.BASE_URL}{Urls.COURIER_URL}",
            data=payload
        )

        assert response2.status_code == 409
        assert "Этот логин уже используется" in response2.text

        delete_courier(login, password)


