import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .ui_utils import print_header, print_info, print_result


@allure.epic("UI Tests")
@allure.feature("Main Page")
@allure.story("Главная страница")
class TestMainPage:
    """Тесты главной страницы."""

    @allure.title("Главная страница")
    @allure.tag("smoke", "main_page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_homepage_load(self, browser, main_page):
        """Проверка загрузки главной страницы."""
        print_header("Главная страница")

        with allure.step("Проверка URL"):
            current_url = browser.current_url
            assert "vkvideo.ru" in current_url
            print_info("Текущий URL", current_url)

        with allure.step("Проверка заголовка"):
            page_title = browser.title
            assert "VK Видео" in page_title
            print_info("Заголовок", page_title)

        print_result()