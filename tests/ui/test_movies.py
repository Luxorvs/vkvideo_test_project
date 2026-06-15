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

        # Шаг 1: Разворачивание меню
        with allure.step("Разворачивание меню"):
            print("   ⏳ Разворачивание меню...")
            expand_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//h4[contains(text(), 'Развернуть') or contains(text(), 'More')]"))
            )
            expand_button.click()
            print("   ✅ Меню развернуто")

        # Шаг 2: Переход в раздел Фильмы и сериалы
        with allure.step("Переход в раздел 'Фильмы и сериалы'"):
            print("   ⏳ Поиск раздела 'Фильмы и сериалы'...")
            section_selector = "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"

            sections = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, section_selector))
            )

            movies_section = [s for s in sections if s.text == "Movies" or s.text == "Фильмы и сериалы"][0]
            movies_section.click()
            print("   ✅ Клик по разделу")

            WebDriverWait(browser, 15).until(EC.url_contains("movies_serials"))
            print_info("URL после перехода", browser.current_url)

        # Шаг 3: Отладка - что есть на странице
        with allure.step("Отладка: анализ страницы"):
            print("   ⏳ Анализ страницы категорий...")
            time.sleep(5)  # Даем странице время на загрузку

            # Проверяем заголовок страницы
            print(f"   📍 Заголовок страницы: {browser.title}")

            # Ищем все возможные категории
            all_divs = browser.find_elements(By.CSS_SELECTOR, "div.vkitImageBaseOverlayItem__root--XaHNe")
            print(f"   📋 Найдено div.vkitImageBaseOverlayItem: {len(all_divs)}")

            # Ищем текст внутри категорий
            category_texts = browser.find_elements(By.CSS_SELECTOR,
                                                   "div.vkitImageBaseOverlayItem__root--XaHNe .vkitTextClamp__root--ewZ0L")
            print(f"   📋 Найдено элементов с текстом категорий: {len(category_texts)}")
            for cat in category_texts[:15]:
                print(f"      - '{cat.text}'")

            # Ищем возможные кнопки/ссылки
            all_links = browser.find_elements(By.TAG_NAME, "a")
            print(f"   📋 Всего ссылок: {len(all_links)}")

            # Проверяем URL
            print(f"   📍 Текущий URL: {browser.current_url}")

        # Шаг 4: Переход в категорию Фантастика
        with allure.step("Переход в категорию 'Фантастика'"):
            print("   ⏳ Поиск категории 'Фантастика'...")

            # Пробуем разные селекторы
            category_selectors = [
                "div.vkitImageBaseOverlayItem__root--XaHNe",
                "a[href*='fantastic']",
                "div[class*='Category']",
                "div[class*='OverlayItem']"
            ]

            for selector in category_selectors:
                elements = browser.find_elements(By.CSS_SELECTOR, selector)
                print(f"   🔍 Селектор '{selector}': найдено {len(elements)} элементов")

            # Ищем категорию по тексту
            category_elements = browser.find_elements(By.CSS_SELECTOR,
                                                      "div.vkitImageBaseOverlayItem__root--XaHNe .vkitTextClamp__root--ewZ0L")

            for cat in category_elements:
                print(f"      - '{cat.text}'")

            # Ищем "Fantastic" или "Фантастика"
            fantastic_category = None
            for cat in category_elements:
                if cat.text == "Fantastic" or cat.text == "Фантастика":
                    fantastic_category = cat
                    break

            if fantastic_category:
                print(f"   ✅ Найдена категория: {fantastic_category.text}")
                parent_div = fantastic_category.find_element(By.XPATH, "../../..")
                parent_div.click()
                print("   ✅ Клик по категории")
            else:
                print("   ❌ Категория 'Fantastic/Фантастика' не найдена")
                raise AssertionError("Категория не найдена")

            WebDriverWait(browser, 15).until(EC.url_contains("fantastic"))
            print_info("URL после перехода в категорию", browser.current_url)

        # Шаг 5: Получение первого видео
        with allure.step("Получение первого видео"):
            print("   ⏳ Поиск видео...")

            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/video']"))
            )

            video_info = main_page.get_first_video_info()
            if video_info:
                print_info("Название", video_info['title'])
                print_info("URL", video_info['url'])
            else:
                print("   ⚠️ Видео не найдены")

        print_result()