import allure
import requests
from constants import Urls


@allure.step("Создание заказа")
def create_order(payload):
    return requests.post(
        f"{Urls.BASE_URL}{Urls.ORDER_URL}",
        json=payload
    )


@allure.step("Получение списка заказов")
def get_orders_list():
    return requests.get(
        f"{Urls.BASE_URL}{Urls.ORDERS_LIST_URL}"
    )


