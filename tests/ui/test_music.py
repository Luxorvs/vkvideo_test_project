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

        # Шаг 1: Переход в раздел Музыка
        with allure.step("Переход в раздел Музыка"):
            section_selector = "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"

            # Находим и кликаем по разделу Музыка
            sections = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, section_selector))
            )
            music_section = [s for s in sections if "Музыка" in s.text][0]
            music_section.click()

            WebDriverWait(browser, 10).until(
                EC.url_contains("musical")
            )
            print_info("URL раздела", browser.current_url)

        # Шаг 2: Получение первого видео
        with allure.step("Получение первого видео"):
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/video']"))
            )

            video_info = main_page.get_first_video_info()
            print_info("Название", video_info['title'])
            print_info("URL", video_info['url'])

        print_result()