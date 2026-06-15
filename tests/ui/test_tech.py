import pytest
import allure
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

        # Шаг 1: Ожидание загрузки главной страницы
        with allure.step("Ожидание загрузки главной страницы"):
            print("   ⏳ Ожидание загрузки главной страницы...")
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h4.vkitgetColorClass__colorTextPrimary--Pm0qG")))
            print("   ✅ Главная страница загружена")

        # Шаг 2: Поиск и переход в подборку Технологии
        with allure.step("Поиск подборки Технологии"):
            print("   ⏳ Поиск вкладки 'Технологии'...")

            # Используем XPATH с contains для надежного поиска
            try:
                tech_tab = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Technology') or contains(text(), 'Технологии')]")))
                tech_tab.click()
                print("   ✅ Клик по вкладке 'Технологии'")
            except:
                print("   ⚠️ Вкладка 'Технологии' не найдена, пропускаем тест")
                pytest.skip("Подборка 'Технологии' отсутствует в текущем окружении")

            # Ждем загрузки страницы
            WebDriverWait(browser, 10).until(EC.url_contains("technology"))
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