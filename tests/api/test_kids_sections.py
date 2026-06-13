import allure
import logging
from tests.api.conftest import API_VERSION, CLIENT_ID, ACCESS_TOKEN, format_videos

logger = logging.getLogger(__name__)


@allure.epic("API Tests")
@allure.feature("POST requests")
@allure.story("Kids Section")
@allure.title('Get videos from "For kids" - Recommended section')
@allure.tag("API", "POST", "kids")
@allure.severity('critical')
@allure.label("owner", "Dmitriy")
def test_get_for_kids_recommended_videos(api_request):
    """Тест получения видео из раздела Для детей - блок Рекомендации"""

    response = api_request(
        "/catalog.getVideoShowcase",
        params={"v": API_VERSION, "client_id": CLIENT_ID},
        data={"url": "https://vkvideo.ru/for_kids", "need_blocks": 1, "access_token": ACCESS_TOKEN}
    )
    assert response.status_code == 200

    body = response.json()

    videos_dict = {v["id"]: v for v in body["response"]["videos"]}
    for_kids_section = next(s for s in body["response"]["catalog"]["sections"] if s["title"] == "For kids")
    target_block = next(
        b for b in for_kids_section["blocks"] if b["data_type"] == "videos" and b["title"] == "Recommended")

    videos = [videos_dict[int(vid.split("_")[1])] for vid in target_block["videos_ids"]]

    format_videos(videos, limit=10, section_name="Для детей - Recommended")