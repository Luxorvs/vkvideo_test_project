import pytest
import allure
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

        # Шаг 1: Переход в раздел Детям (без разворачивания меню)
        with allure.step("Переход в раздел 'Детям'"):
            print("   ⏳ Поиск раздела 'Детям'...")
            section_selector = "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"

            sections = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, section_selector)))

            kids_section = [s for s in sections if s.text == "For kids" or s.text == "Детям"][0]
            kids_section.click()
            print("   ✅ Клик по разделу")

            WebDriverWait(browser, 15).until(EC.url_contains("for_kids"))
            print_info("URL раздела", browser.current_url)

        # Шаг 2: Переход в категорию Развивашки
        with allure.step("Переход в категорию 'Развивашки'"):
            print("   ⏳ Поиск категории 'Развивашки'...")

            # Скролл для подгрузки категорий
            browser.execute_script("window.scrollBy(0, 300);")
            WebDriverWait(browser, 3).until(lambda d: d.execute_script("return document.readyState") == "complete")

            category_selector = "div.vkitImageBaseOverlayItem__root--XaHNe .vkitTextClamp__root--ewZ0L"
            category_elements = WebDriverWait(browser, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, category_selector)))

            developmental_category = \
            [c for c in category_elements if c.text == "Developmental" or c.text == "Развивашки"][0]
            print(f"   ✅ Найдена категория: {developmental_category.text}")

            parent_div = developmental_category.find_element(By.XPATH, "../../..")
            parent_div.click()
            print("   ✅ Категория выбрана")

            WebDriverWait(browser, 15).until(EC.url_contains("education"))
            print_info("URL категории", browser.current_url)

        # Шаг 3: Получение первого видео
        with allure.step("Получение первого видео"):
            print("   ⏳ Поиск видео...")

            WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.vkitVideoCardInfoLayout__titleLink--44M2B")))

            videos = browser.find_elements(By.CSS_SELECTOR, "a.vkitVideoCardInfoLayout__titleLink--44M2B")
            first_video = videos[0]
            title = first_video.get_attribute('title') or first_video.text
            url = first_video.get_attribute('href')

            print_info("Название", title)
            print_info("URL", url)

        print_result()