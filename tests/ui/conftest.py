import pytest
import allure
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

    # Проверяем нужно ли использовать Selenoid
    use_selenoid = os.getenv("USE_SELENOID", "false").lower() == "true"

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
    else:
        print("Running locally")
        driver = webdriver.Chrome(options=chrome_options)

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
    page.open()
    return page