import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TestUser:
    """Тестовый пользователь."""
    email: str
    password: str
    name: Optional[str] = None
    phone: Optional[str] = None


class Config:
    """Основная конфигурация тестов."""

    # Базовые URL
    BASE_URL = os.getenv("BASE_URL", "https://vkvideo.ru")
    SEARCH_URL = BASE_URL + "/?q="

    # Таймауты
    class Timeouts:
        IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
        EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "15"))
        PAGE_LOAD = int(os.getenv("PAGE_LOAD", "30"))
        VIDEO_LOAD = int(os.getenv("VIDEO_LOAD", "45"))
        VIDEO_PLAY = int(os.getenv("VIDEO_PLAY", "20"))
        FILTER_APPLY_WAIT = int(os.getenv("FILTER_APPLY_WAIT", "10"))

    # Тестовые данные
    TEST_SEARCH_QUERIES: List[str] = [
        "мафия",
        "россия",
        "привет",
        "котики",
        "костер"
    ]

    # Пути
    class Paths:
        SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "./screenshots/")
        ALLURE_DIR = os.getenv("ALLURE_DIR", "./allure-results/")
        LOGS_DIR = os.getenv("LOGS_DIR", "./logs/")
        DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads/")

    # Selenoid конфигурация
    class Selenoid:
        ENABLED = os.getenv("SELENOID_ENABLED", "false").lower() == "true"
        HUB_URL = os.getenv("SELENOID_HUB_URL", "http://localhost:4444/wd/hub")
        VIDEO_ENABLED = os.getenv("SELENOID_VIDEO", "true").lower() == "true"
        ENABLE_VNC = os.getenv("SELENOID_VNC", "true").lower() == "true"
        SCREEN_RESOLUTION = os.getenv("SCREEN_RESOLUTION", "1920x1080x24")

    # Браузер
    BROWSER = os.getenv("BROWSER", "chrome")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

    @classmethod
    def create_dirs(cls):
        """Создание необходимых директорий."""
        for dir_path in [cls.Paths.SCREENSHOT_DIR, cls.Paths.ALLURE_DIR,
                        cls.Paths.LOGS_DIR, cls.Paths.DOWNLOAD_DIR]:
            os.makedirs(dir_path, exist_ok=True)