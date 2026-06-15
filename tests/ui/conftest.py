import pytest
import allure
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage


@pytest.fixture(scope="function")
def browser():
    """
    Фикстура браузера.
    По умолчанию - локальный Chrome.
    Для Selenoid: установить переменную USE_SELENOID=true
    """
    print("\nstart browser for test..")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--lang=ru-RU")

    # Маскируем автоматизацию
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    use_selenoid = os.getenv("USE_SELENOID", "false").lower() == "true"

    print(f"USE_SELENOID = {use_selenoid}")

    if use_selenoid:
        print("Running on Selenoid")
        chrome_options.set_capability("browserName", "chrome")
        chrome_options.set_capability("browserVersion", "127.0")
        chrome_options.set_capability("selenoid:options", {
            "enableVNC": True,
            "enableVideo": True,
        })

        driver = webdriver.Remote(
            command_executor="https://user1:1234@selenoid.autotests.cloud/wd/hub",
            options=chrome_options
        )

        # Удаляем следы автоматизации
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Открываем главную страницу vkvideo.ru
        print("Открываем vkvideo.ru...")
        driver.get("https://vkvideo.ru/")

        # Ждем загрузки страницы
        WebDriverWait(driver, 30).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Ищем и нажимаем кнопку "Продолжить" (капча)
        if use_selenoid:
            # ... код до нажатия кнопки ...
            try:
                print("Поиск кнопки 'Продолжить'...")
                continue_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Продолжить')]"))
                )
                print("Кнопка найдена, нажимаем...")
                continue_button.click()
                print("✅ Кнопка 'Продолжить' нажата!")

                # Ожидание загрузки контента после капчи
                print("⏳ Ожидание загрузки основного контента после капчи...")
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"))
                )
                print("✅ Основной контент загружен!")
                time.sleep(5)  # Дополнительная пауза для стабильности

            except Exception as e:
                print(f"Капча не обнаружена или ошибка: {e}")

    else:
        print("Running locally")
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Ошибка при запуске Chrome: {e}")
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
            except:
                driver = webdriver.Chrome()

    driver.set_page_load_timeout(30)
    driver.base_url = "https://vkvideo.ru"

    yield driver

    allure.attach(
        driver.get_screenshot_as_png(),
        name=f"screenshot",
        attachment_type=allure.attachment_type.PNG
    )

    print("\nquit browser..")
    driver.quit()


@pytest.fixture
def main_page(browser):
    """Фикстура главной страницы."""
    page = MainPage(browser)
    # Для Selenoid страница уже открыта, для локального - открываем
    if os.getenv("USE_SELENOID", "false").lower() != "true":
        page.open()
    return page