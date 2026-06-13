"""
Утилиты для форматирования вывода в UI тестах.
"""
import allure


def print_header(title: str, width: int = 60):
    """
    Выводит заголовок теста в красивом форматировании.
    """
    print("\n" + "=" * width)
    print(f"ТЕСТ: {title.upper()}")
    print("=" * width)

    # Добавляем в Allure
    with allure.step(f"Начало теста: {title}"):
        pass


def print_result(success: bool = True, width: int = 60):
    """
    Выводит результат теста.
    """
    print("\n" + "=" * width)
    print("✅ ТЕСТ ПРОЙДЕН" if success else "❌ ТЕСТ УПАЛ")
    print("=" * width)

    # Добавляем в Allure
    with allure.step("Тест завершен"):
        allure.attach("Успешно" if success else "Провал", name="Результат", attachment_type=allure.attachment_type.TEXT)


def print_subheader(title: str, width: int = 40):
    """
    Выводит подзаголовок (для разделов внутри теста).
    """
    print("\n" + "-" * width)
    print(title)
    print("-" * width)


def print_info(key: str, value: str, indent: int = 3):
    """
    Выводит информацию с отступом.
    """
    print(f"{' ' * indent}{key}: {value}")

    # Добавляем в Allure (без принта)
    allure.attach(value, name=key, attachment_type=allure.attachment_type.TEXT)


def print_pause(seconds: float, message: str = "ПАУЗА ДЛЯ ВИЗУАЛЬНОЙ ПРОВЕРКИ"):
    """
    Выводит сообщение о паузе и делает задержку.
    """
    import time
    print(f"\n{' ' * 3}⏳ {message} ({seconds} секунд)...")
    time.sleep(seconds)
    print(f"{' ' * 3}✅ Проверка завершена")