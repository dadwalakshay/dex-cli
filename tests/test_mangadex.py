import pytest

from dex.integrations import ClientFactory
from dex.integrations.mangadex import MangaDexClient


@pytest.fixture
def manga_data():
    return {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "type": "manga",
        "attributes": {
            "title": {
                "en": "Mock Manga Title",
                "additionalProp2": "string",
                "additionalProp3": "string",
            },
            "altTitles": [
                {
                    "additionalProp1": "string",
                    "additionalProp2": "string",
                    "additionalProp3": "string",
                }
            ],
            "description": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string",
            },
            "isLocked": True,
            "links": {
                "additionalProp1": "string",
                "additionalProp2": "string",
                "additionalProp3": "string",
            },
            "originalLanguage": "string",
            "lastVolume": "string",
            "lastChapter": "string",
            "publicationDemographic": "shounen",
            "status": "completed",
            "year": 0,
            "contentRating": "safe",
            "chapterNumbersResetOnNewVolume": True,
            "latestUploadedChapter": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "tags": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "type": "tag",
                    "attributes": {
                        "name": {
                            "additionalProp1": "string",
                            "additionalProp2": "string",
                            "additionalProp3": "string",
                        },
                        "description": {
                            "additionalProp1": "string",
                            "additionalProp2": "string",
                            "additionalProp3": "string",
                        },
                        "group": "content",
                        "version": 1,
                    },
                    "relationships": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "type": "string",
                            "related": "monochrome",
                            "attributes": {},
                        }
                    ],
                }
            ],
            "state": "draft",
            "version": 1,
            "createdAt": "string",
            "updatedAt": "string",
        },
        "relationships": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "type": "string",
                "related": "monochrome",
                "attributes": {},
            }
        ],
    }


@pytest.fixture
def chapter_data():
    return {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "type": "chapter",
        "attributes": {
            "title": "Mock Chapter Title",
            "volume": "1",
            "chapter": "1",
            "pages": 1,
            "translatedLanguage": "string",
            "uploader": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "externalUrl": "string",
            "version": 1,
            "createdAt": "string",
            "updatedAt": "string",
            "publishAt": "string",
            "readableAt": "string",
        },
        "relationships": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "type": "string",
                "related": "monochrome",
                "attributes": {},
            }
        ],
    }


@pytest.fixture
def chapter_image_data():
    return {
        "result": "ok",
        "baseUrl": "https://uploads.mangadex.org",
        "chapter": {
            "hash": "3303dd03ac8d27452cce3f2a882e94b2",
            "data": [
                "1-f7a76de10d346de7ba01786762ebbedc666b412ad0d4b73baa330a2a392dbcdd.png",
                "2-2a5e95dfec7f15cd01f9a63835be18a22fb77a10fd2d62858c7dcbb6e6c622f9.png",
                "3-d06c6f764fdc3c76ea7ae3b76493fdf1a32b8926f2b60ed207b5c2fed13d002e.png",
                "4-a614d6456b9b13931bc5c5ef23cb5f744671f0e1e08c7335682a32de78482f71.png",
                "5-1105a368fd73ae99a06d7aebd165a1ff4322539ba50022a967f7b5fb0a185ce5.png",
                "6-e8a3eac12d879c541c4a36da550d2c69cc9450cb9b1840a079f890facf5f0c89.png",
            ],
            "dataSaver": [
                "1-27e7476475e60ad4cc4cefdb9b2dce29d84f490e145211f6b2e14b13bdb57f33.jpg",
                "2-b4e2cd69df2648279b7d87d44f7860d3fc760aa442e08c49579359f3cf4b4f14.jpg",
                "3-b45f66bdac44652ea2eae40bb5788afe34b8ab5a66e69f0d406257804ddaeda1.jpg",
                "4-92b328471cca1b032bd99cd8506c945a2c3b5a5fd32275b0c4dbfd8ddcfe7e0a.jpg",
                "5-b2336d540fe4a2f9f452cec8e4b2d2ef894f66535e45a4468bf59a6d37f025fe.jpg",
                "6-09f2deb563e802464c161bf7bfa2b094a4727efb4f962d30cf8ee2857a0a66c8.jpg",
            ],
        },
    }


def test_get_manga_title(manga_data: dict) -> None:
    assert MangaDexClient.get_manga_title(manga_data) == "Mock Manga Title"


def test_get_chapter_title(chapter_data: dict) -> None:
    assert MangaDexClient.get_chapter_title(chapter_data) == "Mock Chapter Title"


def test_get_chapter_volume_num(chapter_data: dict) -> None:
    assert MangaDexClient.get_chapter_volume_num(chapter_data) == "1"


def test_get_chapter_num(chapter_data: dict) -> None:
    assert MangaDexClient.get_chapter_num(chapter_data) == "1"


def test_get_chapter_page_count(chapter_data: dict) -> None:
    assert MangaDexClient.get_chapter_page_count(chapter_data) == 1


def test_get_client_valid() -> None:
    assert isinstance(ClientFactory.get_client("mangadex"), MangaDexClient)


def test_get_client_invalid() -> None:
    with pytest.raises(NotImplementedError) as excinfo:
        ClientFactory.get_client("unsupported-client")

    assert str(excinfo.value) == "Un-supported client."


def test_dl_link_builder(chapter_image_data: dict) -> None:
    assert (
        MangaDexClient.dl_link_builder(
            chapter_image_data["baseUrl"],
            chapter_image_data["chapter"]["hash"],
            chapter_image_data["chapter"]["data"][0],
        )
        == "https://uploads.mangadex.org/data/3303dd03ac8d27452cce3f2a882e94b2/1-f7a76de10d346de7ba01786762ebbedc666b412ad0d4b73baa330a2a392dbcdd.png"
    )
