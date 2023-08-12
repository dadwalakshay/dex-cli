import pytest
from rich.console import Console

from dex.integrations.mangadex import MangaDexClient


@pytest.fixture
def manga_list_success_resp():
    return {
        "result": "ok",
        "response": "collection",
        "data": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "type": "manga",
                "attributes": {
                    "title": {
                        "en": "Mock Anime",
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
        ],
        "limit": 0,
        "offset": 0,
        "total": 0,
    }


@pytest.fixture
def chapter_list_success_resp():
    return {
        "result": "ok",
        "response": "collection",
        "data": [
            {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "type": "chapter",
                "attributes": {
                    "title": "string",
                    "volume": "string",
                    "chapter": "string",
                    "pages": 0,
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
        ],
        "limit": 0,
        "offset": 0,
        "total": 0,
    }


def test_manga_list_success(manga_list_success_resp):
    console = Console()

    assert MangaDexClient.get_manga_choices(manga_list_success_resp, console) == {
        "1": manga_list_success_resp["data"][0],
    }


def test_chapter_list_success(chapter_list_success_resp):
    console = Console()

    assert MangaDexClient.get_chapter_choices(chapter_list_success_resp, console) == {
        "1": chapter_list_success_resp["data"][0],
    }
