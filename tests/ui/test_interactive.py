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

        # Шаг 1: Ожидание загрузки главной страницы
        with allure.step("Ожидание загрузки главной страницы"):
            print("   ⏳ Ожидание загрузки главной страницы...")
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"))
            )
            print("   ✅ Главная страница загружена")
            time.sleep(2)

        # Шаг 2: Разворачивание меню
        with allure.step("Разворачивание меню"):
            print("   ⏳ Поиск кнопки 'Развернуть'...")
            section_selector = "h4.vkitgetColorClass__colorTextPrimary--Pm0qG"
            sections = browser.find_elements(By.CSS_SELECTOR, section_selector)

            # Ищем кнопку "Развернуть" или "More" (для английской версии)
            expand_keywords = ["Развернуть", "More", "Expand"]
            expand_elements = [s for s in sections if any(kw in s.text for kw in expand_keywords)]

            if expand_elements:
                expand_elements[0].click()
                print("   ✅ Меню развернуто")
                time.sleep(3)
            else:
                print("   ⚠️ Кнопка 'Развернуть' не найдена, возможно меню уже развернуто")

        # Шаг 3: Переход в раздел Интерактив (поддержка русского и английского)
        with allure.step("Переход в раздел Интерактив"):
            print("   ⏳ Поиск раздела 'Интерактив'...")
            time.sleep(2)

            sections = browser.find_elements(By.CSS_SELECTOR, section_selector)
            print(f"   📋 Найдено секций: {len(sections)}")

            for s in sections:
                print(f"      - {s.text}")

            # Поиск по русскому или английскому названию
            interactive_keywords = ["Интерактив", "Interactive"]
            interactive_elements = [s for s in sections if any(kw in s.text for kw in interactive_keywords)]

            if not interactive_elements:
                print("   ❌ Раздел 'Интерактив' не найден!")
                raise AssertionError("Раздел 'Интерактив' не найден на странице")

            interactive_section = interactive_elements[0]
            interactive_section.click()
            print("   ✅ Клик по разделу 'Интерактив'")

            # Ожидание загрузки страницы раздела
            print("   ⏳ Ожидание загрузки страницы раздела...")
            WebDriverWait(browser, 15).until(EC.url_contains("interactives"))
            time.sleep(3)
            print_info("URL раздела", browser.current_url)

        # Шаг 4: Переход в подраздел От сообществ
        with allure.step("Переход в подраздел От сообществ"):
            print("   ⏳ Поиск вкладки 'От сообществ'...")
            WebDriverWait(browser, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.vkuiTabsItem__host"))
            )

            # Поиск по русскому или английскому названию
            tabs = browser.find_elements(By.CSS_SELECTOR, "a.vkuiTabsItem__host, span.vkuiTabsItem__label")
            community_tab = None
            for tab in tabs:
                tab_text = tab.text
                if "От сообществ" in tab_text or "Communities" in tab_text:
                    community_tab = tab
                    break

            if community_tab:
                community_tab.click()
            else:
                # Fallback по data-testid
                community_tab = WebDriverWait(browser, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='tab-/interactives/communities']"))
                )
                community_tab.click()

            print("   ✅ Клик по вкладке 'От сообществ'")

            # Ожидание загрузки страницы подраздела
            print("   ⏳ Ожидание загрузки страницы подраздела...")
            WebDriverWait(browser, 15).until(EC.url_contains("communities"))
            time.sleep(3)
            print_info("URL подраздела", browser.current_url)

        # Шаг 5: Сбор разделов
        with allure.step("Сбор разделов"):
            print("   ⏳ Скролл страницы...")
            browser.execute_script("window.scrollBy(0, 300);")
            time.sleep(3)

            print("   ⏳ Поиск видео карточек...")
            titles = WebDriverWait(browser, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='video_card_title']"))
            )
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