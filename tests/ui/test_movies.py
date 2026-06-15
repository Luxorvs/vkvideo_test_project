import pytest
import allure
import time
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

        # Шаг 1: Поиск раздела Фильмы и сериалы (с поддержкой английского)
        with allure.step("Поиск раздела 'Фильмы и сериалы'"):
            section_selector = "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"

            # Ждем загрузки секций
            sections = WebDriverWait(browser, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, section_selector))
            )

            # Ищем раздел по русскому или английскому названию
            section_keywords = ["Фильмы и сериалы", "Movies", "Movies and series", "TV series"]
            movies_section = None

            for s in sections:
                for kw in section_keywords:
                    if kw in s.text:
                        movies_section = s
                        break
                if movies_section:
                    break

            if not movies_section:
                raise AssertionError("Раздел 'Фильмы и сериалы' не найден")

            print(f"   ✅ Найден раздел: {movies_section.text}")
            movies_section.click()

            WebDriverWait(browser, 15).until(
                EC.url_contains("movies_serials")
            )
            print_info("URL после перехода", browser.current_url)
            time.sleep(2)

        # Шаг 2: Ожидание загрузки категорий
        with allure.step("Ожидание загрузки категорий"):
            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.vkitImageBaseOverlayItem__root--XaHNe"))
            )
            print("   ✅ Категории загружены")
            time.sleep(2)

        # Шаг 3: Поиск категории Фантастика
        with allure.step("Поиск категории 'Фантастика'"):
            category_selector = "div.vkitImageBaseOverlayItem__root--XaHNe .vkitTextClamp__root--ewZ0L"
            categories = WebDriverWait(browser, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, category_selector))
            )

            # Ищем категорию по русскому или английскому названию
            category_keywords = ["Фантастика", "Fantastic", "Sci-fi", "Science fiction"]
            fantastic_category = None

            for c in categories:
                for kw in category_keywords:
                    if kw in c.text:
                        fantastic_category = c
                        break
                if fantastic_category:
                    break

            if not fantastic_category:
                print("   ⚠️ Категория 'Фантастика' не найдена, пробуем первую...")
                fantastic_category = categories[0]

            print(f"   ✅ Найдена категория: {fantastic_category.text}")

            # Кликаем по родительскому элементу
            parent_div = fantastic_category.find_element(By.XPATH, "../../..")
            parent_div.click()

            WebDriverWait(browser, 15).until(
                EC.url_contains("fantastic")
            )
            print_info("URL после перехода в категорию", browser.current_url)
            time.sleep(2)

        # Шаг 4: Проверка финального URL
        with allure.step("Проверка финального URL"):
            final_url = browser.current_url
            assert "fantastic" in final_url or "fantastik" in final_url.lower()
            print_info("Финальный URL", final_url)

        # Шаг 5: Получение первого видео
        with allure.step("Получение первого видео"):
            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/video']"))
            )
            time.sleep(2)

            video_info = main_page.get_first_video_info()
            if video_info:
                print_info("Название", video_info['title'])
                print_info("URL", video_info['url'])
            else:
                print("   ⚠️ Видео не найдены")

        print_result()