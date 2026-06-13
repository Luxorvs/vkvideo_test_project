import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .ui_utils import print_header, print_info, print_result, print_pause


@allure.epic("UI Tests")
@allure.feature("Search Filters")
@allure.story("Фильтрация контента")
class TestSearchFilters:
    """Тесты фильтров поиска."""

    @allure.title("Поиск с фильтрами")
    @allure.tag("smoke", "filters", "regression")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_with_filters(self, browser, main_page):
        """Тест: поиск 'костер' с применением фильтров."""
        print_header("Поиск с фильтрами")

        # Шаг 1: Поиск
        with allure.step("Поиск по запросу 'костер'"):
            search_input = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']"))
            )
            search_input.clear()
            search_input.send_keys("костер")
            search_input.send_keys("\ue007")
            time.sleep(3)

        # Шаг 2: Открыть фильтры
        with allure.step("Открытие панели фильтров"):
            filter_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Все фильтры']/.."))
            )
            filter_button.click()
            print("   ✅ Фильтры открыты")
            time.sleep(2)

        # Шаг 3: Применение фильтров
        with allure.step("Выбор фильтра: Сортировка → По длительности"):
            time.sleep(1)
            filter_elements = browser.find_elements(By.CSS_SELECTOR, "span.vkuiSubnavigationButton__label")
            filter_el = [el for el in filter_elements if "Сортировка" in el.text][0]
            filter_el.click()
            print("         ✓ Фильтр 'Сортировка' нажат")
            time.sleep(1)
            option = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='По длительности']"))
            )
            option.click()
            print("         ✓ Выбрано: По длительности")
            time.sleep(1)

        with allure.step("Выбор фильтра: Тип контента → Видео"):
            time.sleep(1)
            filter_elements = browser.find_elements(By.CSS_SELECTOR, "span.vkuiSubnavigationButton__label")
            filter_el = [el for el in filter_elements if "Тип контента" in el.text][0]
            filter_el.click()
            print("         ✓ Фильтр 'Тип контента' нажат")
            time.sleep(1)
            option = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Видео']"))
            )
            option.click()
            print("         ✓ Выбрано: Видео")
            time.sleep(1)

        with allure.step("Выбор фильтра: Длительность → Короткие"):
            time.sleep(1)
            filter_elements = browser.find_elements(By.CSS_SELECTOR, "span.vkuiSubnavigationButton__label")
            filter_el = [el for el in filter_elements if "Длительность" in el.text][0]
            filter_el.click()
            print("         ✓ Фильтр 'Длительность' нажат")
            time.sleep(1)
            option = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Короткие']"))
            )
            option.click()
            print("         ✓ Выбрано: Короткие")
            time.sleep(1)

        with allure.step("Включение фильтра: Высокое качество"):
            filter_elements = browser.find_elements(By.CSS_SELECTOR, "span.vkuiSubnavigationButton__label")
            quality_el = [el for el in filter_elements if "Высокое качество" in el.text][0]
            quality_el.click()
            print("         ✓ Фильтр 'Высокое качество' включен")
            time.sleep(3)

        # Шаг 4: Результаты поиска
        with allure.step("Результаты поиска (первые 5 видео)"):
            time.sleep(2)
            videos = browser.find_elements(By.CSS_SELECTOR, "a.vkitVideoCardInfoLayout__titleLink--44M2B")[:5]

            videos_info = []
            for i, video in enumerate(videos, 1):
                title = video.get_attribute('title') or video.text

                parent = video.find_element(By.XPATH, "./ancestor::div[contains(@class, 'VideoCard')]")
                views_elem = parent.find_element(By.CSS_SELECTOR, "[data-testid='video_card_additional_info']")
                views = views_elem.text

                videos_info.append(f"{i}. {title} (Просмотры: {views})")
                print(f"\n   {i}. {title}")
                print(f"      Просмотры: {views}")

            allure.attach(
                "\n".join(videos_info),
                name="первые пять видео",
                attachment_type=allure.attachment_type.TEXT
            )

        print_pause(3, "ФИНАЛЬНАЯ ПРОВЕРКА")
        print_result()