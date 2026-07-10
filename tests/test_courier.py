import allure
import pytest
import requests
from constants import Urls
from helpers.helpers import generate_random_string
from api.courier_api import create_courier, create_courier_with_payload, login_courier, delete_courier_by_id


#Создать курьера
@allure.feature('Создание курьера')
class TestCourier:

    @allure.title('Создание курьера с валидными данными')
    @allure.story('Позитивный сценарий')
    def test_create_courier_success(self, delete_courier):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        response = create_courier(login, password, first_name)

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

        response = create_courier_with_payload(payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"


    @allure.title('Создание курьера с уже существующим логином')
    @allure.story('Негативный сценарий')
    def test_create_courier_duplicate_login(self, delete_courier):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)

        response1 = create_courier(login, password, first_name)
        assert response1.status_code == 201

        response2 = create_courier(login, password, first_name)
        assert response2.status_code == 409
        assert response2.json()["message"] == "Этот логин уже используется. Попробуйте другой."

        delete_courier(login, password)


