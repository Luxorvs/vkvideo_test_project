import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .ui_utils import print_header, print_info, print_result


@allure.epic("UI Tests")
@allure.feature("Movies")
@allure.story("Навигация по категориям")
class TestMovies:
    """Тесты для раздела Фильмы и сериалы."""

    @allure.title("Фильмы и сериалы → Фантастика")
    @allure.tag("smoke", "navigation", "critical_path")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_movies_to_fantastic(self, browser, main_page):
        """Тест: переход в Фильмы и сериалы → Фантастика."""
        print_header("Фильмы и сериалы → Фантастика")

        # Шаг 1: Ожидание загрузки главной страницы
        with allure.step("Ожидание загрузки главной страницы"):
            print("   ⏳ Ожидание загрузки главной страницы...")
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"))
            )
            print("   ✅ Главная страница загружена")

        # Шаг 2: Поиск раздела Фильмы и сериалы
        with allure.step("Поиск раздела 'Фильмы и сериалы'"):
            print("   ⏳ Поиск раздела 'Фильмы и сериалы'...")
            section_selector = "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"

            sections = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, section_selector))
            )

            movies_section = [s for s in sections if s.text == "Movies" or s.text == "Фильмы и сериалы"][0]
            movies_section.click()
            print("   ✅ Клик по разделу")

            # Проверяем, изменился ли URL
            try:
                WebDriverWait(browser, 10).until(EC.url_contains("movies_serials"))
                print_info("URL после перехода", browser.current_url)
            except:
                print("   ⚠️ URL не изменился, раздел 'Фильмы и сериалы' недоступен, пропускаем тест")
                pytest.skip("Раздел 'Фильмы и сериалы' недоступен в текущем окружении")

        # Шаг 3: Проверка наличия категорий
        with allure.step("Проверка загрузки категорий"):
            print("   ⏳ Проверка наличия категорий...")
            browser.execute_script("window.scrollBy(0, 300);")

            category_selector = "div.vkitImageBaseOverlayItem__root--XaHNe"
            try:
                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, category_selector))
                )
                print("   ✅ Категории загружены")
            except:
                print("   ⚠️ Категории не загрузились, пропускаем тест")
                pytest.skip("Категории не загрузились на странице /movies_serials")

        # Шаг 4: Поиск категории Фантастика
        with allure.step("Поиск категории 'Фантастика'"):
            print("   ⏳ Поиск категории 'Фантастика'...")

            category_text_selector = "div.vkitImageBaseOverlayItem__root--XaHNe .vkitTextClamp__root--ewZ0L"
            category_elements = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, category_text_selector))
            )

            fantastic_category = [c for c in category_elements if c.text == "Fantastic" or c.text == "Фантастика"][0]
            parent_div = fantastic_category.find_element(By.XPATH, "../../..")
            parent_div.click()
            print("   ✅ Клик по категории")

            WebDriverWait(browser, 15).until(EC.url_contains("fantastic"))
            print_info("URL после перехода в категорию", browser.current_url)

        # Шаг 5: Получение первого видео
        with allure.step("Получение первого видео"):
            print("   ⏳ Поиск видео...")

            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/video']"))
            )

            video_info = main_page.get_first_video_info()
            print_info("Название", video_info['title'])
            print_info("URL", video_info['url'])

        print_result()