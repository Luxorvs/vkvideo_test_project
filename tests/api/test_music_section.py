import allure
import logging
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
    assert response.status_code == 200

    # Находим блок "Top releases" с типом videos
    sections = response.json()["response"]["catalog"]["sections"]
    music_section = next(s for s in sections if s["id"] == MUSIC_SECTION_ID)

    target_block = next(
        b for b in music_section["blocks"]
        if b.get("title") == "Top releases" and b.get("data_type") == "videos"
    )

    # Получаем видео из блока
    response = api_request(
        "/video.getCatalogBlockItems",
        params={"v": API_VERSION, "client_id": CLIENT_ID},
        data={"block_id": target_block["id"], "access_token": ACCESS_TOKEN}
    )
    assert response.status_code == 200

    # Валидация и вывод
    body = response.json()
    validate(body, music_block_response_schema)

    videos = body["response"]["videos"]

    format_videos(videos, limit=5, section_name="Top Releases")