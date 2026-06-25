import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .ui_utils import print_header, print_info, print_result, print_pause
from .settings import Config


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

        # Используем таймауты из конфига
        element_timeout = Config.Timeouts.EXPLICIT_WAIT

        # Шаг 1: Поиск
        with allure.step("Поиск по запросу 'костер'"):
            search_input = WebDriverWait(browser, element_timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search']"))
            )
            search_input.clear()
            search_input.send_keys("костер")
            search_input.send_keys("\ue007")
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/video']"))
            )

        # Шаг 2: Тип контента → Видео
        with allure.step("Выбор фильтра: Тип контента → Видео"):
            filter_elements = WebDriverWait(browser, element_timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.vkuiSubnavigationButton__label"))
            )
            filter_el = [el for el in filter_elements if "Тип контента" in el.text or "Content type" in el.text][0]
            filter_el.click()
            print("         ✓ Фильтр 'Тип контента' нажат")

            option = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Видео' or text()='Videos']"))
            )
            option.click()
            print("         ✓ Выбрано: Видео (Videos)")

            # Пауза между нажатиями
            print("\n   ⏳ Пауза 1.5 секунды между нажатиями...")
            time.sleep(1.5)

        # Шаг 3: Длительность → Короткие
        with allure.step("Выбор фильтра: Длительность → Короткие"):
            filter_elements = WebDriverWait(browser, element_timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.vkuiSubnavigationButton__label"))
            )
            filter_el = [el for el in filter_elements if "Длительность" in el.text or "Duration" in el.text][0]
            filter_el.click()
            print("         ✓ Фильтр 'Длительность' нажат")

            option = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Короткие' or text()='Short']"))
            )
            option.click()
            print("         ✓ Выбрано: Короткие (Short)")

            # Пауза между нажатиями
            print("\n   ⏳ Пауза 1.5 секунды между нажатиями...")
            time.sleep(1.5)

        # Шаг 4: Сортировка → По дате
        with allure.step("Выбор фильтра: Сортировка → По дате"):
            filter_elements = WebDriverWait(browser, element_timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.vkuiSubnavigationButton__label"))
            )
            filter_el = [el for el in filter_elements if "Сортировка" in el.text or "Sort by" in el.text][0]
            filter_el.click()
            print("         ✓ Фильтр 'Сортировка' нажат")

            option = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='По дате' or text()='Date']"))
            )
            option.click()
            print("         ✓ Выбрано: По дате (Date)")

            # Пауза между нажатиями
            print("\n   ⏳ Пауза 1.5 секунды между нажатиями...")
            time.sleep(1.5)

        # Шаг 5: Высокое качество
        with allure.step("Включение фильтра: Высокое качество"):
            filter_elements = WebDriverWait(browser, element_timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.vkuiSubnavigationButton__label"))
            )
            quality_el = [el for el in filter_elements if "Высокое качество" in el.text or "High quality" in el.text][0]
            quality_el.click()
            print("         ✓ Фильтр 'Высокое качество' включен (High quality)")

            # Пауза после последнего нажатия
            time.sleep(2)

        # Шаг 6: Результаты поиска
        with allure.step("Результаты поиска (первые 5 видео)"):
            videos = WebDriverWait(browser, element_timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.vkitVideoCardInfoLayout__titleLink--44M2B"))
            )[:5]

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