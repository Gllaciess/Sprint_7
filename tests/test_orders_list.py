import allure
from api.order_api import get_orders_list


@allure.feature('Список заказов')
class TestOrdersList:

    @allure.title('Получение списка заказов')
    @allure.story('Позитивный сценарий')
    def test_orders_list(self):

        response = get_orders_list()


        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)


        