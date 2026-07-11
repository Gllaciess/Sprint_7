import pytest
import requests
from constants import Urls


@pytest.fixture
def delete_courier():
    courier_ids = []

    def _delete_courier(login, password):
        response = requests.post(
            f"{Urls.BASE_URL}{Urls.LOGIN_URL}",
            data={"login": login, "password": password}
        )
        if response.status_code == 200:
            courier_id = response.json().get("id")
            if courier_id:
                courier_ids.append(courier_id)

    yield _delete_courier

    for courier_id in courier_ids:
        requests.delete(f"{Urls.BASE_URL}{Urls.COURIER_URL}/{courier_id}")

        
