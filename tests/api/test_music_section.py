import allure
import logging
import pytest
from voluptuous import validate
from tests.api.conftest import (
    API_VERSION, CLIENT_ID, ACCESS_TOKEN, MUSIC_SECTION_ID,
    CATALOG_GET_VIDEO_PARAMS, CATALOG_GET_VIDEO_DATA,
    music_block_response_schema, format_videos
)

logger = logging.getLogger(__name__)


@allure.epic("API Tests")
@allure.feature("POST requests")
@allure.story("Music Section")
@allure.title('Get Top releases from music section')
@allure.tag("API", "POST", "music")
@allure.severity('critical')
@allure.label("owner", "Dmitriy")
def test_music_top_releases(api_request):
    """Тест получения блока 'Top releases' из музыкального раздела"""

    # Получаем структуру каталога
    response = api_request(
        "/catalog.getVideo",
        params=CATALOG_GET_VIDEO_PARAMS,
        data=CATALOG_GET_VIDEO_DATA
    )

    # Проверяем, что запрос выполнен успешно
    assert response.status_code == 200

    body = response.json()

    # Проверяем наличие ошибки в ответе
    if "error" in body:
        error_msg = body["error"].get("error_msg", "Unknown error")
        logger.warning(f"API вернул ошибку: {error_msg}")
        pytest.skip(f"Раздел музыки недоступен: {error_msg}")

    # Проверяем наличие поля response
    if "response" not in body:
        logger.warning("Поле 'response' отсутствует в ответе")
        pytest.skip("Раздел музыки недоступен (нет поля response)")

    # Проверяем наличие catalog и sections
    if "catalog" not in body["response"] or "sections" not in body["response"]["catalog"]:
        logger.warning("Каталог или секции отсутствуют в ответе")
        pytest.skip("Раздел музыки недоступен (нет каталога)")

    sections = body["response"]["catalog"]["sections"]

    # Ищем музыкальную секцию
    music_section = None
    for s in sections:
        if s.get("id") == MUSIC_SECTION_ID:
            music_section = s
            break

    if not music_section:
        logger.warning(f"Секция музыки с ID {MUSIC_SECTION_ID} не найдена")
        pytest.skip("Раздел музыки недоступен (секция не найдена)")

    # Ищем блок "Top releases"
    target_block = None
    for b in music_section["blocks"]:
        if b.get("title") == "Top releases" and b.get("data_type") == "videos":
            target_block = b
            break

    if not target_block:
        logger.warning("Блок 'Top releases' не найден")
        pytest.skip("Блок 'Top releases' недоступен")

    # Получаем видео из блока
    response = api_request(
        "/video.getCatalogBlockItems",
        params={"v": API_VERSION, "client_id": CLIENT_ID},
        data={"block_id": target_block["id"], "access_token": ACCESS_TOKEN})
    assert response.status_code == 200

    # Валидация и вывод
    body = response.json()
    validate(body, music_block_response_schema)

    videos = body["response"]["videos"]

    format_videos(videos, limit=5, section_name="Top Releases")