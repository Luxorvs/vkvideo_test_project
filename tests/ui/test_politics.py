import pytest
import allure
import time
from selenium.webdriver.common.by import By
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
            time.sleep(1)

        # Шаг 2: Переход в подкатегорию Популярное
        with allure.step("Переход в подкатегорию Популярное"):
            # Ищем заголовок
            titles = browser.find_elements(By.CSS_SELECTOR, "span[data-testid='carousel-title']")
            popular_title = [t for t in titles if "Популярное" in t.text][0]
            print(f"      ✅ Найден заголовок: {popular_title.text}")

            # Ищем ссылку "Показать все"
            all_links = browser.find_elements(By.TAG_NAME, "a")
            show_all_link = [l for l in all_links if l.is_displayed() and "Показать все" in l.text][0]
            show_all_link.click()
            time.sleep(2)

            print_info("URL подкатегории", browser.current_url)

        # Шаг 3: Получение первого видео
        with allure.step("Получение первого видео"):
            video_info = main_page.get_first_video_info()
            assert video_info is not None, "Видео не найдены"
            print_info("Название", video_info['title'])
            print_info("URL", video_info['url'])

        print_result()