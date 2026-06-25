import pytest
import allure
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

        # Шаг 1: Ожидание загрузки главной страницы
        with allure.step("Ожидание загрузки главной страницы"):
            print("   ⏳ Ожидание загрузки главной страницы...")
            WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h4.vkitgetColorClass__colorTextPrimary--Pm0qG")))
            print("   ✅ Главная страница загружена")

        # Шаг 2: Разворачивание меню (клик по "Развернуть" или "More")
        with allure.step("Разворачивание меню"):
            print("   ⏳ Разворачивание меню...")
            expand_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//h4[contains(text(), 'Развернуть') or contains(text(), 'More')]")))
            expand_button.click()
            print("   ✅ Меню развернуто")

        # Шаг 3: Переход в раздел Интерактив
        with allure.step("Переход в раздел Интерактив"):
            print("   ⏳ Поиск раздела 'Интерактив'...")
            section_selector = "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"

            sections = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, section_selector)))

            interactive_section = [s for s in sections if s.text == "Interactive" or s.text == "Интерактив"][0]
            interactive_section.click()
            print("   ✅ Клик по разделу")

            WebDriverWait(browser, 15).until(EC.url_contains("interactives"))
            print_info("URL раздела", browser.current_url)

        # Шаг 4: Переход в подраздел От сообществ
        with allure.step("Переход в подраздел От сообществ"):
            print("   ⏳ Поиск вкладки 'От сообществ'...")

            # Используем data-testid (работает и на Selenoid, и локально)
            community_tab = WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tab-/interactives/communities']")))
            community_tab.click()
            print("   ✅ Клик по вкладке")

            WebDriverWait(browser, 15).until(EC.url_contains("communities"))
            print_info("URL подраздела", browser.current_url)

        # Шаг 5: Сбор разделов
        with allure.step("Сбор разделов"):
            browser.execute_script("window.scrollBy(0, 300);")
            WebDriverWait(browser, 3).until(lambda d: d.execute_script("return document.readyState") == "complete")

            titles = WebDriverWait(browser, 15).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='video_card_title']")))
            print(f"   ✅ Найдено разделов: {len(titles)}")

            print_subheader("ПЕРВЫЕ 5 ИНТЕРАКТИВНЫХ РАЗДЕЛОВ")

            sections_info = []
            for i in range(min(5, len(titles))):
                title_elem = titles[i]
                title = title_elem.get_attribute('title') or title_elem.text
                sections_info.append(f"{i + 1}. {title}")
                print(f"\n   {i + 1}. {title}")

            allure.attach(
                "\n".join(sections_info),
                name="первые пять разделов",
                attachment_type=allure.attachment_type.TEXT
            )

        print_result()