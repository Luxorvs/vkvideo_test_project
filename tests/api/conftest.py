import pytest
import allure
import requests
import logging
from datetime import datetime
from voluptuous import Schema, Required, All, Length, Range, Optional, validate

# ========== НАСТРОЙКА ЛОГИРОВАНИЯ ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ========== КОНСТАНТЫ ==========
BASE_API_URL = "https://api.vkvideo.ru"
BASE_WEB_URL = "https://vkvideo.ru"

API_VERSION = "5.280"
CLIENT_ID = "52461373"
ACCESS_TOKEN = "anonym.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhbm9ueW1faWQiOjI0MTkzOTIwNywiYXBwX2lkIjo1MjQ2MTM3MywiaWF0IjoxNzgxNTExNDQ3LCJpc192ZXJpZmllZCI6ZmFsc2UsImV4cCI6MTc4MTU5Nzg0Nywic2lnbmVkX3RpbWUiOm51bGwsImFub255bV9pZF9sb25nIjo5MTE2MzQ5MTk0MzExMzU4NDEyLCJzY29wZSI6Nzg4MTI5OTM0Nzg5ODM2OH0.bZn8ISvljLk30q6Squkf4OzIMNNyv9PsFXgMKK2osO4"

# Разделы для политики
POLITIC_SECTIONS = {
    "Популярное": "PUlQVA8GR0R3W0tMF0QECi8fABVGaxsJNh4FF0cWR0RzSVNUQUYOCCIYS1oXAElcdFpFVAQBSVx3Fg",
    "Новости": "PUlQVA8GR0R3W0tMF0QECi8fABVGawUDMRhLWhcBSVxkHxsTW1AYRGpJXVQPBlpKZFpcVA8FFg",
    "Интервью": "PUlQVA8GR0R3W0tMF0QECi8fABVGawIIMg4bAFxRHERqSVxUDxYfFCMFDQUXGElSZFFbRxkWWlNkUVgL",
    "Шоу": "PUlQVA8GR0R3W0tMF0QECi8fABVGaxgOKRxLWhcBSVxkHxsTW1AYRGpJXVQPBlpKZFpcVA8FFg",
    "Документальное": "PUlQVA8GR0R3W0tMF0QECi8fABVGaw8JJR4EE1tAChQ_SUVUABZRRDIZDBhRR0lKZF9LTAcFR0R3XktMBEk"
}

# ID секций для catalog.getSection
SECTION_IDS = {
    "Авто": "PUldVA8AR0RzSVNUWFUCCBkKHAJaWQQSLx0MVBkWUkR8WhQ",
    "Еда": "PUldVA8AR0RzSVNUWFUCCBkIBhleXQUBZEdLTxcOWhs"
}

# ID раздела Музыка
MUSIC_SECTION_ID = "PUldVA8AR0RzSVNUWEEYDyUKBVQZFlJEfFoU"

# Параметры для catalog.getVideo
CATALOG_GET_VIDEO_PARAMS = {
    "v": API_VERSION,
    "client_id": CLIENT_ID
}

CATALOG_GET_VIDEO_DATA = {
    "url": f"{BASE_WEB_URL}/musical",
    "need_blocks": "1",
    "access_token": ACCESS_TOKEN
}


# ========== ФИКСТУРА ==========
@pytest.fixture
def api_request():
    """Фикстура для API запросов с логированием"""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": BASE_WEB_URL,
        "Referer": f"{BASE_WEB_URL}/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    })

    call_count = 0

    def _request(endpoint, data=None, params=None, log=True):
        nonlocal call_count
        call_count += 1

        url = f"{BASE_API_URL}/method{endpoint}"

        logger.info(f"REQUEST: {endpoint} | Params: {params} | Data: {data}")

        start_time = datetime.now()
        response = session.post(url, params=params, data=data)
        elapsed_time = (datetime.now() - start_time).total_seconds()

        logger.info(f"RESPONSE: {response.status_code} | Time: {elapsed_time:.2f}s | URL: {url}")

        if log and call_count == 1:
            allure.attach(f"{response.request.method} {endpoint}", name="Request URL",
                          attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(dict(params or {}) | (data or {})), name="Request Data",
                          attachment_type=allure.attachment_type.TEXT)
            allure.attach(str(response.status_code), name="Response Status",
                          attachment_type=allure.attachment_type.TEXT)

            try:
                response_json = response.json()
                allure.attach(str(response_json), name="Response Body", attachment_type=allure.attachment_type.JSON)
            except:
                allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)

        return response

    return _request


# ========== ОБЩАЯ ФУНКЦИЯ ФОРМАТИРОВАНИЯ ==========
def format_videos(videos, limit=5, section_name=""):
    """Форматирование видео для Allure отчета"""
    output_lines = []
    for i, video in enumerate(videos[:limit], 1):
        owner_id = video.get("owner_id", 0)
        video_id = video.get("id", 0)
        title = video.get('title', 'Без названия')[:70]
        output_lines.append(f"{i}. {title}\n   🔗 https://vkvideo.ru/video-{abs(owner_id)}_{video_id}")

    output = "\n\n".join(output_lines)
    attach_name = f"📹 {section_name}" if section_name else "📹 Videos"
    allure.attach(output, name=attach_name, attachment_type=allure.attachment_type.TEXT)
    logger.info(f"Formatted {len(videos[:limit])} videos for section: {section_name}")

    return output


# ========== СХЕМЫ ДЛЯ REQUEST ==========
def validate_request(data, schema):
    """Валидация request данных"""
    from voluptuous import MultipleInvalid
    try:
        validate(data, schema)
        logger.info(f"Request validation passed: {list(data.keys())}")
    except MultipleInvalid as e:
        logger.error(f"Request validation failed: {e}")
        raise


catalog_get_section_request_schema = Schema({
    Required('v'): str,
    Required('client_id'): str,
    Required('section_id'): str,
    Required('access_token'): str
})

video_get_catalog_block_items_request_schema = Schema({
    Required('v'): str,
    Required('client_id'): str,
    Required('block_id'): str,
    Required('access_token'): str
})

# ========== СХЕМЫ ДЛЯ RESPONSE ==========
video_schema = Schema({
    Required('id'): All(int, Range(min=1)),
    Required('title'): All(str, Length(min=1)),
    Required('owner_id'): int,
    Required('duration'): int,
    Required('views'): int,
    Required('image'): list,
    Required('track_code'): str
})

video_response_schema = Schema({
    Required('response'): {
        Required('videos'): [video_schema],
        Required('count'): int,
        Required('next_from'): str
    }
})

music_block_response_schema = video_response_schema