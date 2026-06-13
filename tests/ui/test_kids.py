import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .ui_utils import print_header, print_info, print_result


@allure.epic("UI Tests")
@allure.feature("Kids")
@allure.story("Детский контент")
class TestKids:
    """Тесты для раздела Детям."""

    @allure.title("Детям → Развивашки")
    @allure.tag("smoke", "kids", "navigation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_kids_educational(self, browser, main_page):
        """Тест: Детям → Развивашки → первое видео."""
        print_header("Детям → Развивашки")

        # Шаг 1: Переход в раздел Детям
        with allure.step("Переход в раздел Детям"):
            main_page.go_to_section("Детям")
            print_info("URL раздела", browser.current_url)

        # Шаг 2: Переход в категорию Развивашки
        with allure.step("Переход в категорию Развивашки"):
            browser.execute_script("window.scrollBy(0, 300);")

            category_selector = "div.vkitImageBaseOverlayItem__root--XaHNe .vkitTextClamp__root--ewZ0L"
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, category_selector))
            )

            category_elements = browser.find_elements(By.CSS_SELECTOR, category_selector)
            developing_category = [c for c in category_elements if "Развивашки" in c.text][0]

            parent_div = developing_category.find_element(By.XPATH, "../../..")
            parent_div.click()
            print("   ✅ Категория 'Развивашки' найдена")

            WebDriverWait(browser, 10).until(
                EC.url_contains("education")
            )
            print_info("URL категории", browser.current_url)

        # Шаг 3: Получение первого видео
        with allure.step("Получение первого видео"):
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