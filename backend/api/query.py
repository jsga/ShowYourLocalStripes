import logging
from typing import List, Union

import sqlalchemy
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select, SelectOfScalar
from sqlalchemy.sql import text

from .models import Item, Store
from .utils import slack_send

logger = logging.getLogger(__name__)
SelectOfScalar.inherit_cache = True  # type: ignore
Select.inherit_cache = True  # type: ignore

AllowedDBSchemas = Union[Store, Item]


async def select_by_id(
    session: AsyncSession,
    schema: AllowedDBSchemas,
    filter_id: Union[List[Union[int, str]], Union[int, str]],
    name_key: Union[List[str], str] = "id",
) -> List[AllowedDBSchemas]:
    """Selects item, filtered by a given key"""

    statement = select(schema)
    if isinstance(filter_id, list) and isinstance(name_key, list):
        for id, key in zip(filter_id, name_key):
            statement = statement.filter(getattr(schema, key) == id)
    else:
        statement = statement.filter(getattr(schema, name_key) == filter_id)
    statement_results = await session.execute(statement)
    query_results = statement_results.all()

    return query_results


def sync_insert_or_update(
    db_engine: sqlalchemy.engine.Engine,
    row: AllowedDBSchemas,
    name_key: Union[str, List[str]],
) -> None:
    """Inserts an item or updates if exists"""

    with Session(db_engine) as session:
        statement = select(type(row)).filter(
            getattr(type(row), name_key) == getattr(row, name_key)
        )
        query_results = session.exec(statement).all()

        if len(query_results) > 1:
            msg = f"ERROR! >0 results. {query_results=}"
            logger.error(msg)
            slack_send(msg)

        elif len(query_results) == 1:
            # Update
            for k, v in query_results[0].dict().items():
                if k not in name_key:
                    setattr(query_results[0], k, getattr(row, k))
        else:
            # Insert
            session.add(row)
        session.commit()


async def insert_or_update(
    session: AsyncSession,
    row: AllowedDBSchemas,
    name_key: Union[str, List[str]],
) -> None:
    """Inserts an item or updates if exists"""

    statement = select(type(row)).filter(
        getattr(type(row), name_key) == getattr(row, name_key)
    )
    query_results_ = await session.execute(statement)
    query_results = query_results_.all()

    if len(query_results) > 1:
        msg = f"ERROR! >0 results. {query_results=}"
        logger.error(msg)
        slack_send(msg)

    elif len(query_results) == 1:
        # Update
        for k, v in query_results[0][0].dict().items():
            if k not in name_key:
                setattr(query_results[0][0], k, getattr(row, k))
    else:
        # Insert
        session.add(row)
    await session.commit()


async def get_n_stores(session: AsyncSession, n=10):
    statement = (
        select([Store.location, Store.lat, Store.lon])
        .group_by(Store.location, Store.lat, Store.lon)
        .order_by(text("random()"))
        .limit(n)
    )

    query_results_ = await session.execute(statement)
    return query_results_.all()
