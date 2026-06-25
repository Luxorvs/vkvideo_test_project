import pytest
import allure
import time
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
            section_selector = "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"

            sections = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, section_selector)))

            # Ищем раздел "Политика" или "Politics"
            politics_section = None
            for s in sections:
                if s.text == "Политика" or s.text == "Politics":
                    politics_section = s
                    break

            if not politics_section:
                print("   ⚠️ Раздел 'Политика' не найден, пропускаем тест")
                pytest.skip("Раздел 'Политика' отсутствует в текущем окружении")

            politics_section.click()
            print("   ✅ Клик по разделу")

            WebDriverWait(browser, 15).until(EC.url_contains("politics"))
            print_info("URL раздела", browser.current_url)
            time.sleep(1)

        # Шаг 2: Переход в подкатегорию Популярное (просто добавляем /popular к URL)
        with allure.step("Переход в подкатегорию Популярное"):
            current_url = browser.current_url
            popular_url = current_url.rstrip('/') + "/popular"
            browser.get(popular_url)

            WebDriverWait(browser, 15).until(EC.url_contains("popular"))
            print_info("URL подкатегории", browser.current_url)
            time.sleep(2)

        # Шаг 3: Получение первого видео
        with allure.step("Получение первого видео"):
            WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/video']")))

            video_info = main_page.get_first_video_info()
            if video_info:
                print_info("Название", video_info['title'])
                print_info("URL", video_info['url'])
            else:
                print("   ⚠️ Видео не найдены")

        print_result()