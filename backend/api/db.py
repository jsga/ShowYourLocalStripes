from sys import modules

from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncEngine, AsyncSession

from .settings import settings

if "pytest" in modules:
    db_connection_str = settings.TEST_DB_URI
else:
    db_connection_str = settings.ASYNC_DB_URI.get_secret_value()

engine = AsyncEngine(
    create_engine(settings.ASYNC_DB_URI.get_secret_value(), echo=False, future=True)
)


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


def create_db_engine(echo: bool = False):
    """Sync definition of engine"""

    engine = create_engine(settings.SYNC_DB_URI.get_secret_value(), echo=echo)

    return engine
