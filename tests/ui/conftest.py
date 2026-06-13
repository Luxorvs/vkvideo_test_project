import pytest
import allure
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.main_page import MainPage


def pytest_addoption(parser):
    """Добавление опций командной строки для выбора окружения."""
    parser.addoption(
        "--env",
        action="store",
        default="local",
        help="Environment to run tests: local or selenoid"
    )
    parser.addoption(
        "--selenoid-url",
        action="store",
        default=os.getenv("SELENOID_URL", "http://localhost:4444/wd/hub"),
        help="Selenoid hub URL"
    )


@pytest.fixture(scope="function")
def browser(request):
    """
    Фикстура браузера с поддержкой локального и удаленного запуска.
    """
    env = request.config.getoption("--env")
    selenoid_url = request.config.getoption("--selenoid-url")

    print(f"\nstart browser for test.. (env: {env})")

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--lang=ru-RU")

    if env == "selenoid":
        # Настройки для Selenoid (Selenium 4 синтаксис)
        chrome_options.set_capability("browserName", "chrome")
        chrome_options.set_capability("browserVersion", "120.0")
        chrome_options.set_capability("selenoid:options", {
            "enableVNC": True,
            "enableVideo": True,
            "name": request.node.name
        })

        driver = webdriver.Remote(
            command_executor=selenoid_url,
            options=chrome_options
        )
    else:
        # Локальный запуск
        driver = webdriver.Chrome(options=chrome_options)

    driver.set_page_load_timeout(30)
    driver.base_url = "https://vkvideo.ru"

    yield driver

    allure.attach(
        driver.get_screenshot_as_png(),
        name=f"screenshot_{request.node.name}",
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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для сохранения результата теста.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        item.rep_call = rep