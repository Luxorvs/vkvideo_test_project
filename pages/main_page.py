import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class MainPage(BasePage):
    """
    PageObject для главной страницы и результатов поиска.
    """

    # Локаторы
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='search'], input[name='q']")
    SECTION_SELECTOR = "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"
    CATEGORY_SELECTOR = "div.vkitImageBaseOverlayItem__root--XaHNe .vkitTextClamp__root--ewZ0L"

    def __init__(self, browser):
        super().__init__(browser, "https://vkvideo.ru/")

    @allure.step("Открытие главной страницы")
    def open(self):
        """Открывает главную страницу."""
        self.browser.get(self.url)
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.SECTION_SELECTOR))
        )
        return self

    @allure.step("Поиск видео по запросу '{query}'")
    def search_for(self, query: str):
        """Выполнение поиска через Enter."""
        search_input = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
        )
        search_input.clear()
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)

        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/video']"))
        )
        return self

    @allure.step("Перейти в раздел {section_name}")
    def go_to_section(self, section_name: str):
        """Переход в указанный раздел с автоматическим раскрытием меню."""
        # Разворачиваем меню если нужно
        try:
            expand = self.browser.find_element(By.XPATH, "//*[contains(text(), 'Развернуть')]")
            if expand.is_displayed():
                expand.click()
                print(f"   ✅ Меню развернуто")
                time.sleep(1)
        except:
            pass

        # Ищем раздел
        sections = self.browser.find_elements(By.CSS_SELECTOR, self.SECTION_SELECTOR)
        section_element = [s for s in sections if section_name in s.text][0]
        print(f"   ✅ Найден раздел: {section_element.text}")

        # Пробуем кликнуть по ссылке или по элементу
        try:
            link = section_element.find_element(By.XPATH, "./..")
            href = link.get_attribute('href')
            if href:
                self.browser.get(href)
            else:
                section_element.click()
        except:
            section_element.click()

        # Ждем изменения URL
        WebDriverWait(self.browser, 10).until(
            lambda driver: driver.current_url != "https://vkvideo.ru/"
        )
        return self

    @allure.step("Кликнуть на категорию {category_name}")
    def click_category(self, category_name: str):
        """Клик по категории."""
        # Прокручиваем страницу
        self.browser.execute_script("window.scrollBy(0, 300);")
        time.sleep(1)

        # Ищем категорию
        category_elements = self.browser.find_elements(By.CSS_SELECTOR, self.CATEGORY_SELECTOR)
        category_element = [c for c in category_elements if category_name in c.text][0]
        print(f"   ✅ Найдена категория: {category_element.text}")

        # Находим кликабельный родитель
        parent_div = category_element.find_element(By.XPATH, "../../..")
        self.browser.execute_script("arguments[0].scrollIntoView(true);", parent_div)
        time.sleep(1)

        # Кликаем
        parent_div.click()
        print(f"   ✅ Клик по категории выполнен")

        # Ждем изменения URL
        WebDriverWait(self.browser, 10).until(
            EC.url_contains(category_name.lower())
        )
        return self

    @allure.step("Получение информации о первом видео")
    def get_first_video_info(self) -> dict:
        """
        Получает информацию о первом видео (URL и название).
        """
        # Ждем появления видео
        WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/video']"))
        )
        time.sleep(1)

        # Ищем видео несколькими селекторами
        video_selectors = [
            "a.vkitVideoCardInfoLayout__titleLink--44M2B",
            "a.VideoCard__title",
            "a[class*='videoCard']",
            "a[href*='/video']"
        ]

        for selector in video_selectors:
            video_links = self.browser.find_elements(By.CSS_SELECTOR, selector)
            for link in video_links:
                if link.is_displayed():
                    url = link.get_attribute('href')
                    if url and '/video' in url and 'playlist' not in url:
                        title = link.get_attribute('title') or link.text
                        if title:
                            title = ' '.join(title.split())
                            return {'url': url, 'title': title}

        return None