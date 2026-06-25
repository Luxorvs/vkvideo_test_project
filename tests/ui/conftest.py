import pytest
import allure
import os
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.main_page import MainPage

warnings.filterwarnings("ignore", category=UserWarning, module="selenium.webdriver.remote.remote_connection")


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

    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    use_selenoid = os.getenv("USE_SELENOID", "false").lower() == "true"

    print(f"USE_SELENOID = {use_selenoid}")

    if use_selenoid:
        print("Running on Selenoid")
        chrome_options.set_capability("browserName", "chrome")
        chrome_options.set_capability("browserVersion", "128.0")
        chrome_options.set_capability("selenoid:options", {
            "enableVNC": True,
            "enableVideo": False,
        })

        driver = webdriver.Remote(
            command_executor="https://user1:1234@selenoid.autotests.cloud/wd/hub",
            #command_executor="http://ru.selenoid.autotests.cloud/wd/hub",
            options=chrome_options
        )

        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print("Открываем vkvideo.ru...")
        driver.get("https://vkvideo.ru/")

        WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")

        try:
            continue_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Продолжить')]")))
            print("Обнаружена капча, нажимаем 'Продолжить'...")
            continue_button.click()
            print("✅ Капча пройдена!")
        except:
            pass

        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h4.vkitgetColorClass__colorTextPrimary--Pm0qG")))
        print("✅ Основной контент загружен!")

    else:
        print("Running locally")
        try:
            driver = webdriver.Chrome(options=chrome_options)
        except:
            from webdriver_manager.chrome import ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

        # Для локального запуска тоже открываем страницу
        print("Открываем vkvideo.ru...")
        driver.get("https://vkvideo.ru/")
        WebDriverWait(driver, 30).until(lambda d: d.execute_script("return document.readyState") == "complete")
        print("✅ Страница загружена!")

    driver.set_page_load_timeout(60)
    driver.base_url = "https://vkvideo.ru"

    yield driver

    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"screenshot",
            attachment_type=allure.attachment_type.PNG
        )
    except:
        pass

    print("\nquit browser..")
    driver.quit()


@pytest.fixture
def main_page(browser):
    """Фикстура главной страницы."""
    from pages.main_page import MainPage
    page = MainPage(browser)
    return page