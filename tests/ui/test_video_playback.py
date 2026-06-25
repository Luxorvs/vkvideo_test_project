import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.custom_video_player import CustomVideoPlayer
from .ui_utils import print_header, print_info, print_result, print_pause


@allure.epic("UI Tests")
@allure.feature("Video Playback")
@allure.story("Воспроизведение видео")
class TestVideoPlayback:
    """Тесты воспроизведения видео."""

    @allure.title("Воспроизведение видео")
    @allure.tag("smoke", "video", "critical")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_video_playback(self, browser, main_page):
        """Тест: поиск видео и управление с клавиатуры."""
        print_header("Воспроизведение видео")

        # Шаг 1: Поиск видео
        with allure.step("Поиск видео по запросу 'котики'"):
            main_page.search_for("котики")
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/video']")))
            print("   ✅ Результаты поиска загружены")

        # Шаг 2: Получение первого видео
        with allure.step("Получение первого видео"):
            video_info = main_page.get_first_video_info()
            print_info("Название", video_info['title'])
            print_info("URL видео", video_info['url'])

        # Шаг 3: Открытие видео
        with allure.step("Открытие видео"):
            browser.get(video_info['url'])
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class*='VideoPlayer']")))
            print_pause(5, "ЗАГРУЗКА СТРАНИЦЫ")

        # Шаг 4: Управление с клавиатуры
        with allure.step("Управление с клавиатуры"):
            player = CustomVideoPlayer(browser)
            player.test_keyboard_controls()

        print_result()