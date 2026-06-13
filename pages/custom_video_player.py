import time
import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


class CustomVideoPlayer:
    """Класс для управления видеоплеером VK Video."""

    def __init__(self, browser):
        self.browser = browser
        self.actions = ActionChains(browser)

    def find_video_container(self):
        """Находит контейнер видео."""
        selectors = [
            "div[class*='VideoPlayer']",
            "div[class*='videoplayer']",
            "div[class*='VideoContainer']",
            "div[data-testid*='player']",
            "video"
        ]

        for selector in selectors:
            try:
                elements = self.browser.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    if element.is_displayed():
                        return element
            except:
                continue
        return None

    def hover_over_video(self):
        """Наводит курсор на видео."""
        with allure.step("Наведение курсора на видео"):
            container = self.find_video_container()
            if container:
                self.actions.move_to_element(container).perform()
                time.sleep(1)
                print("   ✓ Курсор наведен")
                return True
            return False

    def test_keyboard_controls(self):
        """
        Тестирование всех клавиш с паузами.
        """
        with allure.step("Ожидание загрузки видео (реклама)"):
            print("   ⏳ Ожидание 19 секунд (реклама и загрузка)...")
            time.sleep(19)

        # Наводим курсор на видео для фокуса
        self.hover_over_video()
        time.sleep(1)

        # Пауза (пробел)
        with allure.step("Нажатие ПРОБЕЛ (пауза)"):
            self.actions.send_keys(Keys.SPACE).perform()
            print("   ✓ ПРОБЕЛ (пауза)")
            time.sleep(3)

        # Полноэкранный режим (F)
        with allure.step("Нажатие F (полный экран)"):
            self.actions.send_keys('f').perform()
            print("   ✓ F (полный экран)")
            time.sleep(3)

        # Пробуем ESC несколькими способами
        with allure.step("Нажатие ESC (выход из полноэкранного режима)"):
            print("   ⏳ Выход из полноэкранного режима...")
            self.actions.send_keys(Keys.ESCAPE).perform()
            time.sleep(1)
            self.browser.execute_script("document.exitFullscreen();")
            time.sleep(1)
            self.actions.send_keys(Keys.ESCAPE).perform()
            print("   ✓ ESC")

        # Снова наводим курсор
        self.hover_over_video()
        time.sleep(1)

        # Запуск видео (пробел)
        with allure.step("Нажатие ПРОБЕЛ (запуск видео)"):
            self.actions.send_keys(Keys.SPACE).perform()
            print("   ✓ ПРОБЕЛ (запуск)")
            time.sleep(3)

        return True