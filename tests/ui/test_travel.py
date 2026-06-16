import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .ui_utils import print_header, print_info, print_result


@allure.epic("UI Tests")
@allure.feature("Travel")
@allure.story("Путешествия")
class TestTravel:
    """Тесты для подборки Путешествия."""

    @allure.title("Подборка Путешествия")
    @allure.tag("smoke", "travel", "collections")
    @allure.severity(allure.severity_level.NORMAL)
    def test_travel_collection(self, browser, main_page):
        """Тест: подборка Путешествия → первое видео."""
        print_header("Подборка Путешествия")

        # Шаг 1: Ожидание загрузки главной страницы
        with allure.step("Ожидание загрузки главной страницы"):
            print("   ⏳ Ожидание загрузки главной страницы...")
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h4.vkitgetColorClass__colorTextPrimary--Pm0qG")))
            print("   ✅ Главная страница загружена")

        # Шаг 2: Поиск и переход в подборку Путешествия
        with allure.step("Поиск подборки Путешествия"):
            print("   ⏳ Поиск вкладки 'Путешествия'...")

            travel_tab = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH,"//span[contains(text(), 'Travel') or contains(text(), 'Путешествия') or contains(text(), 'Tourisme')]")))
            travel_tab.click()
            print("   ✅ Клик по вкладке 'Путешествия'")

            WebDriverWait(browser, 10).until(EC.url_contains("tourisme"))
            print_info("URL подборки", browser.current_url)

        # Шаг 3: Получение первого видео
        with allure.step("Получение первого видео"):
            print("   ⏳ Поиск первого видео...")

            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.vkitVideoCardInfoLayout__titleLink--44M2B")))

            videos = browser.find_elements(By.CSS_SELECTOR, "a.vkitVideoCardInfoLayout__titleLink--44M2B")
            first_video = videos[0]
            title = first_video.get_attribute('title') or first_video.text
            url = first_video.get_attribute('href')

            print_info("Название", title)
            print_info("URL", url)

        print_result()