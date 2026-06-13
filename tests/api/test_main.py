import allure
import re
import requests
import logging
from tests.api.conftest import BASE_WEB_URL

logger = logging.getLogger(__name__)


@allure.epic("API Tests")
@allure.feature("GET requests")
@allure.story("Main Page")
@allure.title('Get VK Video main page (HTML)')
@allure.tag("API", "GET", "main_page")
@allure.severity('critical')
@allure.label("owner", "Dmitriy")
def test_main_page_html():
    """GET тест: получение главной страницы"""

    logger.info(f"GET request to {BASE_WEB_URL}/")
    response = requests.get(f"{BASE_WEB_URL}/")
    logger.info(f"Response status: {response.status_code}")

    assert response.status_code == 200

    title = re.search(r'<title>(.*?)</title>', response.text).group(1)
    logger.info(f"Page title: {title}")
    allure.attach(title, "Page Title", attachment_type=allure.attachment_type.TEXT)
    assert "VK Видео" in title

    # Дополнительно проверяем с параметром format=json
    logger.info(f"GET request to {BASE_WEB_URL}/?format=json")
    response_json = requests.get(f"{BASE_WEB_URL}/", params={"format": "json"})
    logger.info(f"Response status: {response_json.status_code}")
    assert response_json.status_code == 200