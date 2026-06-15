import pytest
import allure
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.main_page import MainPage



@pytest.fixture(scope='function')
def setup_browser(request):
    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "128.0",
        "selenoid:options": {
            "enableVideo": False
        }
    }
    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor="https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options = options
    )

    browser = Browser(Config(driver))
    yield browser


@pytest.fixture(scope="function")
def browser(request):
    """
    Фикстура браузера с поддержкой локального и удаленного запуска.
    """
    env = request.config.getoption("--env")

    if env == "selenoid":
        # Используем вашу существующую фикстуру setup_browser
        from .conftest import setup_browser
        driver = setup_browser(request)
    else:
        # Локальный запуск
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-notifications")
        options.add_argument("--lang=ru-RU")
        driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(30)
    driver.base_url = "https://vkvideo.ru"

    yield driver

    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"screenshot_{request.node.name}_failed",
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