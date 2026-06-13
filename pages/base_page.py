import allure
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Tuple, Optional


class BasePage:
    """
    Базовый класс для всех PageObject.
    """

    def __init__(self, browser: WebDriver, url: str = ""):
        self.browser = browser
        self.url = url
        self.wait = WebDriverWait(browser, 10)

    @allure.step("Открытие страницы")
    def open(self) -> None:
        """Открывает страницу по URL."""
        if self.url:
            self.browser.get(self.url)
        else:
            print("   ⚠️ URL не указан, страница не открыта")

    @allure.step("Поиск элемента {locator}")
    def find_element(self, locator: Tuple[str, str], timeout: int = 10) -> Optional[WebElement]:
        """Поиск элемента с ожиданием."""
        try:
            wait = WebDriverWait(self.browser, timeout)
            return wait.until(EC.presence_of_element_located(locator))
        except:
            return None

    @allure.step("Поиск всех элементов {locator}")
    def find_elements(self, locator: Tuple[str, str], timeout: int = 10) -> List[WebElement]:
        """Поиск всех элементов с ожиданием."""
        try:
            wait = WebDriverWait(self.browser, timeout)
            return wait.until(EC.presence_of_all_elements_located(locator))
        except:
            return []

    @allure.step("Клик по элементу {locator}")
    def click(self, locator: Tuple[str, str]) -> bool:
        """Клик по элементу."""
        element = self.find_element(locator)
        if element:
            element.click()
            return True
        return False

    @allure.step("Ввод текста '{text}' в элемент {locator}")
    def input_text(self, locator: Tuple[str, str], text: str) -> bool:
        """Ввод текста в поле."""
        element = self.find_element(locator)
        if element:
            element.clear()
            element.send_keys(text)
            return True
        return False

    @allure.step("Проверка видимости элемента {locator}")
    def is_element_visible(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Проверка видимости элемента."""
        try:
            wait = WebDriverWait(self.browser, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False

    @allure.step("Получение текущего URL")
    def get_current_url(self) -> str:
        """Получение текущего URL."""
        return self.browser.current_url

    @allure.step("Открыть главную страницу")
    def open_main_page(self):
        """Открывает главную страницу и возвращает MainPage."""
        self.browser.get("https://vkvideo.ru/")
        time.sleep(2)
        from pages.main_page import MainPage
        return MainPage(self.browser)

    def print_result(self):
        """Вывод результата теста."""
        print(f"\n{'='*60}\n✅ ТЕСТ ПРОЙДЕН\n{'='*60}")