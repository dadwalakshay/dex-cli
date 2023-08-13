import pytest

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
