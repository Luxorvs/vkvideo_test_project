import allure
import logging
from voluptuous import validate
from tests.api.conftest import (
    API_VERSION, CLIENT_ID, ACCESS_TOKEN, POLITIC_SECTIONS,
    video_response_schema, format_videos
)

logger = logging.getLogger(__name__)


@allure.epic("API Tests")
@allure.feature("POST requests")
@allure.story("Politics Section")
@allure.title('Get videos from all VK Video sections')
@allure.tag("API", "POST", "politics")
@allure.severity('critical')
@allure.label("owner", "Dmitriy")
def test_get_sections_videos(api_request):
    """Тест получения видео из раздела политика по всем категориям"""

    for section_name, block_id in POLITIC_SECTIONS.items():
        with allure.step(f"Get videos from {section_name}"):
            response = api_request(
                "/video.getCatalogBlockItems",
                params={"v": API_VERSION, "client_id": CLIENT_ID},
                data={"block_id": block_id, "access_token": ACCESS_TOKEN}
            )

            assert response.status_code == 200

            body = response.json()
            validate(body, video_response_schema)

            videos = body["response"]["videos"]
            assert len(videos) > 0

            format_videos(videos, limit=5, section_name=section_name)