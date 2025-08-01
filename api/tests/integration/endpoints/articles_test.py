import pytest

from src.dto.dto_articles import (
    GetArticleResponseMin,
    GetAllArticleResponse,
    GetArticleResponseFull,
)
from tests.integration.endpoints.setup.articles_setup import (
    do_nothing,
    push_one_article_bundle,
    push_ten_articles_bundle,
    push_ten_articles_with_2_categories_bundle,
    TITLE,
    LOGIN,
    LABEL,
    CREATED_AT,
    CONTENT,
)
from tests.utils.utils_client import get_test_client


get_all_params = {
    "zero": {
        "loader": do_nothing,
        "expected": GetAllArticleResponse(
            count=0,
            articles=[],
        ),
    },
    "one": {
        "loader": push_one_article_bundle,
        "expected": GetAllArticleResponse(
            count=1,
            articles=[
                GetArticleResponseMin(
                    id=1,
                    title=TITLE,
                    creator=LOGIN,
                    id_category=1,
                    category=LABEL,
                    created_at=CREATED_AT.isoformat(),
                )
            ],
        ),
    },
    "ten": {
        "loader": push_ten_articles_bundle,
        "expected": GetAllArticleResponse(
            count=10,
            articles=[
                GetArticleResponseMin(
                    id=id + 1,
                    title=f"{TITLE}{id + 1}",
                    creator=f"{LOGIN}",
                    id_category=1,
                    category=LABEL,
                    created_at=CREATED_AT.isoformat(),
                )
                for id in range(10)
            ],
        ),
    },
    "five_filtered_by_category": {
        "route": "/articles/?category_id=1",
        "loader": push_ten_articles_with_2_categories_bundle,
        "expected": GetAllArticleResponse(
            count=5,
            articles=[
                GetArticleResponseMin(
                    id=id + 1,
                    title=f"{TITLE}{id + 1}",
                    creator=f"{LOGIN}",
                    id_category=1,
                    category=f"{LABEL}1",
                    created_at=CREATED_AT.isoformat(),
                )
                for id in range(1, 10 + 1, 2)
            ],
        ),
    },
    "zero_filtered_by_wrong_category": {
        "route": "/articles/?category_id=2",
        "loader": push_one_article_bundle,
        "expected": GetAllArticleResponse(
            count=0,
            articles=[],
        ),
    },
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    get_all_params.values(),
    ids=[f"case_{k}" for k in get_all_params.keys()],
)
async def test_get_all(values: dict):
    route = values.get("route", "/articles/")
    await values["loader"]()
    async with get_test_client() as client:
        response = await client.get(route)
    assert response.status_code == 200
    assert response.json() == values["expected"].model_dump(mode="json")


get_one_params = {
    "found": {
        "loader": push_one_article_bundle,
        "return_code": 200,
        "expected": GetArticleResponseFull(
            id=1,
            title=TITLE,
            id_category=1,
            creator=LOGIN,
            category=LABEL,
            created_at=CREATED_AT.isoformat(),
            content=CONTENT,
        ).model_dump(mode="json"),
    },
    "not_found": {
        "loader": do_nothing,
        "return_code": 404,
        "expected": {"message": "Article introuvable"},
    },
}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "values",
    get_one_params.values(),
    ids=[f"case_{k}" for k in get_one_params.keys()],
)
async def test_get_one(values: dict):
    # Arrange
    route = "/articles/1"
    await values["loader"]()

    # Act
    async with get_test_client() as client:
        response = await client.get(route)

    # Assert
    assert response.status_code == values["return_code"]
    assert response.json() == values["expected"]
