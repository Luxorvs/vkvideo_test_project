import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .ui_utils import print_header, print_info, print_result


@allure.epic("UI Tests")
@allure.feature("Tech")
@allure.story("Технологии")
class TestTech:
    """Тесты для подборки Технологии."""

    @allure.title("Подборка Технологии")
    @allure.tag("smoke", "tech", "collections")
    @allure.severity(allure.severity_level.NORMAL)
    def test_tech_collection(self, browser, main_page):
        """Тест: подборка Технологии → первое видео."""
        print_header("Подборка Технологии")

        # Шаг 1: Поиск и переход в подборку Технологии
        with allure.step("Поиск подборки Технологии"):
            # Ждем загрузки вкладок
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.vkuiTabsItem__label"))
            )

            # Находим все вкладки
            tabs = browser.find_elements(By.CSS_SELECTOR, "span.vkuiTabsItem__label")

            # Ищем вкладку "Технологии"
            tech_tab = [t for t in tabs if "Технологии" in t.text][0]

            # Находим кликабельный родитель и кликаем
            collection_link = tech_tab.find_element(By.XPATH, "./..")
            collection_link.click()
            print("   ✅ Переход в подборку Технологии")

            # Ждем загрузки страницы
            WebDriverWait(browser, 10).until(
                EC.url_contains("technology")
            )
            print_info("URL подборки", browser.current_url)

        # Шаг 2: Получение первого видео
        with allure.step("Получение первого видео"):
            # Ждем появления видео
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.vkitVideoCardInfoLayout__titleLink--44M2B"))
            )

            videos = browser.find_elements(By.CSS_SELECTOR, "a.vkitVideoCardInfoLayout__titleLink--44M2B")
            first_video = videos[0]
            title = first_video.get_attribute('title') or first_video.text
            url = first_video.get_attribute('href')

            print_info("Название", title)
            print_info("URL", url)

        # Пауза для визуальной проверки
        with allure.step("Пауза для визуальной проверки"):
            print("\n   ⏳ Пауза 2 секунды для визуальной проверки...")
            time.sleep(2)
            print("   ✅ Проверка завершена")

        print_result()