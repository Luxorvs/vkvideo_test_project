import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .ui_utils import print_header, print_info, print_result


@allure.epic("UI Tests")
@allure.feature("Politics")
@allure.story("Политический контент")
class TestPolitics:
    """Тесты для раздела Политика."""

    @allure.title("Политика → Популярное")
    @allure.tag("smoke", "politics", "navigation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_politics_popular(self, browser, main_page):
        """Тест: Политика → Популярное → первое видео."""
        print_header("Политика → Популярное")

        # Шаг 1: Переход в раздел Политика
        with allure.step("Переход в раздел Политика"):
            main_page.go_to_section("Политика")
            print_info("URL раздела", browser.current_url)

        # Шаг 2: Переход в подкатегорию Популярное
        with allure.step("Переход в подкатегорию Популярное"):
            # Ищем ссылку "Show all" или "Показать все"
            show_all_link = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Show all') or contains(text(), 'Показать все')]")))
            show_all_link.click()

            # Ждем изменения URL
            WebDriverWait(browser, 15).until(EC.url_contains("popular"))
            print_info("URL подкатегории", browser.current_url)

        # Шаг 3: Получение первого видео
        with allure.step("Получение первого видео"):
            video_info = main_page.get_first_video_info()
            print_info("Название", video_info['title'])
            print_info("URL", video_info['url'])

        print_result()