import pytest
import allure
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
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
        default=os.getenv("SELENOID_URL", "https://user1:1234@selenoid.autotests.cloud/wd/hub"),
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

    # Для CI/CD добавляем headless режим
    if os.getenv("CI") == "true" or os.getenv("HEADLESS") == "true":
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

    if env == "selenoid":
        # Настройки для Selenoid
        chrome_options.set_capability("browserName", "chrome")
        chrome_options.set_capability("browserVersion", "127.0")
        chrome_options.set_capability("selenoid:options", {
            "enableVideo": False
        })

        driver = webdriver.Remote(
            command_executor="https://user1:1234@selenoid.autotests.cloud/wd/hub",
            options=chrome_options
        )
    else:
        # Локальный запуск с автоматической установкой ChromeDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

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