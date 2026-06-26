import allure
import logging
from tests.api.conftest import API_VERSION, CLIENT_ID, ACCESS_TOKEN, SECTION_IDS, format_videos

logger = logging.getLogger(__name__)


@allure.epic("API Tests")
@allure.feature("POST requests")
@allure.story("Food Section")
@allure.title('Get videos from "Food" section')
@allure.tag("API", "POST", "Food")
@allure.severity('critical')
@allure.label("owner", "Dmitriy")
def test_get_cars_section_videos(api_request):
    """Тест получения видео из раздела Авто"""

    response = api_request(
        "/catalog.getSection",
        params={"v": API_VERSION, "client_id": CLIENT_ID},
        data={"section_id": SECTION_IDS["Авто"], "access_token": ACCESS_TOKEN}
    )

    assert response.status_code == 200

    body = response.json()
    videos = {v["id"]: v for v in body["response"]["videos"]}
    block = body["response"]["section"]["blocks"][0]
    video_ids = block["videos_ids"]

    result_videos = [videos[int(vid.split('_')[1])] for vid in video_ids[:10]]

    format_videos(result_videos, limit=10, section_name="Auto - recommendations")