import pytest
import allure
import time
from urllib.parse import unquote
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .ui_utils import print_header, print_info, print_result, print_subheader


@allure.epic("UI Tests")
@allure.feature("Search")
@allure.story("Поиск видео")
class TestSearch:
    """Тесты поиска."""

    @allure.title("Поиск видео")
    @allure.tag("smoke", "search")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_functionality(self, browser, main_page):
        """Проверка поиска по разным запросам."""
        print_header("Поиск видео")

        test_queries = ["мафия", "россия", "привет"]

        for idx, query in enumerate(test_queries, 1):
            print_subheader(f"ЗАПРОС {idx}: '{query.upper()}'")

            with allure.step(f"Поиск по запросу '{query}'"):
                browser.get(f"{browser.base_url}/?q={query}")

                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/video']"))
                )

                current_url = browser.current_url
                assert "?q=" in current_url

                decoded_url = unquote(current_url)
                assert query.lower() in decoded_url.lower()
                print_info("Фактический URL", current_url)
                print("   ✅ Русские буквы обработаны корректно")

            with allure.step("Получение первого видео"):
                first_video = main_page.get_first_video_info()
                print_info("Первое видео", first_video['title'])
                print_info("URL", first_video['url'])

            # Пауза между запросами
            print("\n   ⏳ Пауза 1.5 секунды между запросами...")
            time.sleep(1.5)

        print_result()