import asyncio
from datetime import datetime
from unittest.mock import patch

import pytest
from httpx import AsyncClient

from api.main import app
from api.models import (
    CurrencyResponse,
    ItemsWithColours,
    MessageResponse,
    StoreReadNoPromo,
)

pytestmark = pytest.mark.asyncio

BASE_URL = "http://test"


async def test_get_ping():
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/ping")
    assert response.status_code == 200
    assert response.json() == MessageResponse(data="pong!").dict()


async def test_get_currency(async_session_data):
    with patch("api.currency.datetime") as mock_datetime:
        date_str_now = async_session_data[1]["currency"][0]["modified"]
        date_obj_now = datetime.strptime(date_str_now, "%Y-%m-%d %H:%M:%S.%f")
        mock_datetime.now.return_value = date_obj_now

        async with AsyncClient(app=app, base_url=BASE_URL) as ac:
            response = await ac.get("/currency")

        assert isinstance(CurrencyResponse(**response.json()), CurrencyResponse)
        assert (
            response.json()["gbp_to_eur"]
            == async_session_data[1]["currency"][0]["gbp_to_eur"]
        )


async def test_get_store_status(async_session_data):
    store_id_missing = "2e1ee4ba-xxxx-xxxx-xxxx-d751fa6d6790"
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        ac.get_io_loop = asyncio.get_running_loop
        response = await ac.get(f"/store/status?store_id={store_id_missing}")
    assert response.status_code == 404

    store_from_db_id = async_session_data[1]["store"][0]["id"]
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        ac.get_io_loop = asyncio.get_running_loop
        response = await ac.get(f"/store/status?store_id={store_from_db_id}")
    assert response.status_code == 200
    assert isinstance(ItemsWithColours(**response.json()), ItemsWithColours)


async def test_get_store_random(async_session_data):
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get("/store/random?n=2")
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2
    assert isinstance(StoreReadNoPromo(**data[0]), StoreReadNoPromo)


async def test_get_store_jpg(async_session_data):
    store_from_db_id = async_session_data[1]["store"][0]["id"]
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get(f"/store/image/jpg?store_id={store_from_db_id}")
    assert response.status_code == 200
    # TODO, assert correct image is returned


async def test_get_image(async_session_data):
    store_from_db_id = async_session_data[1]["store"][0]["id"]
    async with AsyncClient(app=app, base_url=BASE_URL) as ac:
        response = await ac.get(f"/store/image?store_id={store_from_db_id}")

    data = response.json()["data"]
    assert data == async_session_data[1]["store"][0]["image_base64"]
    assert isinstance(MessageResponse(data=data), MessageResponse)


@pytest.mark.skip(reason="To do")
async def test_post_store_create():
    # TODO
    pass
