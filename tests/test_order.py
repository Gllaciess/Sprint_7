import allure
import pytest
import requests
from constants import Urls
from helpers.helpers import generate_random_string


@allure.feature('Создание заказа')
class TestOrder:

    @allure.title('Создание заказа с разными вариантами цвета')
    @allure.story('Позитивный сценарий с параметризацией')
    @pytest.mark.parametrize('color', [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_colors(self, color):
        payload = {
            "firstName": generate_random_string(10),
            "lastName": generate_random_string(10),
            "address": "test address",
            "metroStation": 1,
            "phone": "+79001234567",
            "rentTime": 1,
            "deliveryDate": "2025-12-31",
            "comment": "test comment",
            "color": color
        }

        response = requests.post(
            f"{Urls.BASE_URL}{Urls.ORDER_URL}",
            json=payload
        )

        assert response.status_code == 201
        assert "track" in response.json()
        assert response.json()["track"] is not None


        