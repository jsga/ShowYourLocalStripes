import asyncio
import json
from typing import AsyncGenerator, Callable

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from api.models import Colour, Currency, Item, Store
from api.query import insert_or_update
from api.settings import Settings

pytestmark = pytest.mark.anyio
settings = Settings()


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest_asyncio.fixture()
async def db_session() -> AsyncSession:
    async_engine = create_async_engine(
        settings.TEST_DB_URI,
        echo=False,
        future=True,
    )
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)
        async_session = sessionmaker(
            async_engine, class_=AsyncSession, expire_on_commit=False
        )
        async with async_session(bind=conn) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest.fixture()
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest.fixture()
def app(override_get_db: Callable) -> FastAPI:
    from api.db import init_db
    from api.main import app

    app.dependency_overrides[init_db] = override_get_db
    return app


@pytest.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    logger.debug("inside async_client")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


######
@pytest_asyncio.fixture(scope="function")
async def async_session_data() -> tuple:
    # Load seeds data. Order matter.
    tables = [Store, Item, Colour, Currency]
    seeds = {}
    for table in tables:
        with open(f"tests/seeds/{table.__tablename__}.json") as json_file:
            seeds[table.__tablename__] = json.load(json_file)

    # Create tables
    async_engine = create_async_engine(
        settings.ASYNC_DB_URI.get_secret_value(),
        echo=False,
        future=True,
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    # Insert data
    async with sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )() as s:
        for table in tables:
            logger.debug(
                f"Inserting #rows:{len(seeds[table.__tablename__])} in table: "
                f"{table.__tablename__} "
            )
            for x in seeds[table.__tablename__]:
                await insert_or_update(s, table(**x), "id")

    await async_engine.dispose()

    return tables, seeds
