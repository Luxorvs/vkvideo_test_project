import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .ui_utils import print_header, print_info, print_result


@allure.epic("UI Tests")
@allure.feature("Music")
@allure.story("Музыкальный контент")
class TestMusic:
    """Тесты для раздела Музыка."""

    @allure.title("Раздел Музыка")
    @allure.tag("smoke", "music", "navigation")
    @allure.severity(allure.severity_level.NORMAL)
    def test_music_section(self, browser, main_page):
        """Тест: переход в Музыку и первое видео."""
        print_header("Раздел Музыка")

        # Шаг 1: Ожидание загрузки главной страницы
        with allure.step("Ожидание загрузки главной страницы"):
            print("   ⏳ Ожидание загрузки главной страницы...")
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"))
            )
            print("   ✅ Главная страница загружена")

        # Шаг 2: Поиск и переход в раздел Музыка (без разворачивания меню)
        with allure.step("Переход в раздел 'Музыка'"):
            print("   ⏳ Поиск раздела 'Музыка'...")
            section_selector = "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"

            sections = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, section_selector))
            )

            music_section = None
            for s in sections:
                if s.text == "Music" or s.text == "Музыка":
                    music_section = s
                    break

            if not music_section:
                print("   ⚠️ Раздел 'Музыка' не найден, пропускаем тест")
                pytest.skip("Раздел 'Музыка' отсутствует в текущем окружении")

            music_section.click()
            print("   ✅ Клик по разделу")

            WebDriverWait(browser, 15).until(EC.url_contains("musical"))
            print_info("URL раздела", browser.current_url)

        # Шаг 3: Получение первого видео
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