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

        # Шаг 1: Поиск раздела Фильмы и сериалы
        with allure.step("Поиск раздела 'Фильмы и сериалы'"):
            section_selector = "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"
            sections = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, section_selector))
            )

            # Находим нужный раздел
            movies_section = [s for s in sections if "Фильмы и сериалы" in s.text][0]
            movies_section.click()

            WebDriverWait(browser, 10).until(
                EC.url_contains("movies_serials")
            )
            print_info("URL после перехода", browser.current_url)

        # Шаг 2: Ожидание загрузки категорий
        with allure.step("Ожидание загрузки категорий"):
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.vkitImageBaseOverlayItem__root--XaHNe"))
            )
            print("   ✅ Категории загружены")

        # Шаг 3: Поиск категории Фантастика
        with allure.step("Поиск категории 'Фантастика'"):
            category_selector = "div.vkitImageBaseOverlayItem__root--XaHNe .vkitTextClamp__root--ewZ0L"
            categories = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, category_selector))
            )

            # Находим категорию Фантастика
            fantastic_category = [c for c in categories if "Фантастика" in c.text][0]

            # Кликаем по родительскому элементу
            parent_div = fantastic_category.find_element(By.XPATH, "../../..")
            parent_div.click()

            WebDriverWait(browser, 10).until(
                EC.url_contains("fantastic")
            )
            print_info("URL после перехода в категорию", browser.current_url)

        # Шаг 4: Проверка финального URL
        with allure.step("Проверка финального URL"):
            final_url = browser.current_url
            assert "fantastic" in final_url
            print_info("Финальный URL", final_url)

        # Шаг 5: Получение первого видео
        with allure.step("Получение первого видео"):
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/video']"))
            )

            video_info = main_page.get_first_video_info()
            print_info("Название", video_info['title'])
            print_info("URL", video_info['url'])

        print_result()