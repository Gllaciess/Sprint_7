import allure
import requests
from constants import Urls
from helpers.helpers import generate_random_string


@allure.step("Создание данных для курьера")
def register_new_courier_and_return_login_password():
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

    if response.status_code == 201:
        return login, password, first_name
    
    raise Exception(
        f"Не удалось создать курьера. "
        f"Статус: {response.status_code}, "
        f"Тело ответа: {response.text}"
    )


@allure.step("Создание данных для купьера")
def create_courier(login, password, first_name):
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    return requests.post(
        f"{Urls.BASE_URL}{Urls.COURIER_URL}",
        data=payload
    )


@allure.step("Логин для курьера")
def login_courier(login, password):
    payload = {
        "login": login,
        "password": password
    }
    return requests.post(
        f"{Urls.BASE_URL}{Urls.LOGIN_URL}",
        data=payload
    )


@allure.step("Удаление курьера по ID")
def delete_courier_by_id(courier_id):
    return requests.delete(
        f"{Urls.BASE_URL}{Urls.COURIER_URL}/{courier_id}"
    )


@allure.step("Создание курьера с произвольным payload")
def create_courier_with_payload(payload):
    return requests.post(
        f"{Urls.BASE_URL}{Urls.COURIER_URL}",
        data=payload
    )


