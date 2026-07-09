import allure
import requests
from constants import Urls


@allure.feature('Список заказов')
class TestOrdersList:

    @allure.title('Получение списка заказов')
    @allure.story('Позитивный сценарий')
    def test_orders_list(self):
        response = requests.get(f"{Urls.BASE_URL}{Urls.ORDERS_LIST_URL}")

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)


        