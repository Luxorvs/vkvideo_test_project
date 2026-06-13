import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .ui_utils import print_header, print_info, print_result, print_subheader


@allure.epic("UI Tests")
@allure.feature("Interactive")
@allure.story("Навигация по разделам")
class TestInteractive:
    """Тесты для раздела Интерактив."""

    @allure.title("Интерактив → От сообществ")
    @allure.tag("smoke", "navigation", "interactive")
    @allure.severity(allure.severity_level.NORMAL)
    def test_interactive_communities(self, browser, main_page):
        """Тест: Интерактив → От сообществ → список разделов."""
        print_header("Интерактив → От сообществ")

        # Шаг 1: Открытие главной
        with allure.step("Открытие главной страницы"):
            browser.get(browser.base_url)
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"))
            )
            print("   ✅ Главная страница загружена")

        # Шаг 2: Разворачивание меню
        with allure.step("Разворачивание меню"):
            section_selector = "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"
            sections = browser.find_elements(By.CSS_SELECTOR, section_selector)
            expand_section = [s for s in sections if "Развернуть" in s.text][0]
            expand_section.click()
            print("   ✅ Меню развернуто")

        # Шаг 3: Переход в раздел Интерактив
        with allure.step("Переход в раздел Интерактив"):
            time.sleep(1)
            sections = browser.find_elements(By.CSS_SELECTOR, section_selector)
            interactive_section = [s for s in sections if "Интерактив" in s.text][0]
            interactive_section.click()
            print("   ✅ Клик по разделу 'Интерактив'")

            WebDriverWait(browser, 10).until(EC.url_contains("interactives"))
            print_info("URL раздела", browser.current_url)

        # Шаг 4: Переход в подраздел От сообществ
        with allure.step("Переход в подраздел От сообществ"):
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.vkuiTabsItem__host"))
            )
            community_tab = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tab-/interactives/communities']"))
            )
            community_tab.click()
            print("   ✅ Клик по вкладке 'От сообществ'")

            WebDriverWait(browser, 10).until(EC.url_contains("communities"))
            print_info("URL подраздела", browser.current_url)

        # Шаг 5: Сбор разделов
        with allure.step("Сбор разделов"):
            browser.execute_script("window.scrollBy(0, 300);")
            time.sleep(2)

            titles = WebDriverWait(browser, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='video_card_title']"))
            )

            print_subheader("ПЕРВЫЕ 5 ИНТЕРАКТИВНЫХ РАЗДЕЛОВ")

            sections_info = []
            for i in range(5):
                title_elem = titles[i]
                title = title_elem.get_attribute('title') or title_elem.text

                card = title_elem.find_element(By.XPATH, "./ancestor::div[@data-testid='grid-item']")
                duration_elem = card.find_element(By.CSS_SELECTOR, "[data-testid='video_card_additional_info']")
                duration = duration_elem.text

                sections_info.append(f"{i + 1}. {title} (Длительность: {duration})")
                print(f"\n   {i + 1}. {title}")
                print(f"      Длительность: {duration}")

            allure.attach(
                "\n".join(sections_info),
                name="первые пять разделов",
                attachment_type=allure.attachment_type.TEXT
            )

        print_result()