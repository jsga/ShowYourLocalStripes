import base64
import io
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from loguru import logger
from PIL import Image
from sqlmodel.ext.asyncio.session import AsyncSession

from api.currency import currency_conversion
from api.db import get_session, init_db
from api.models import (
    Colour,
    CreateStoreResponse,
    CurrencyResponse,
    Item,
    ItemsWithColours,
    MessageResponse,
    Store,
    StoreRead,
    StoreReadNoPromo,
)
from api.query import get_n_stores, select_by_id
from api.settings import settings
from api.store import create_store_in_db, teemill_post_store
from api.utils import slack_send
from api.weather import create_image

logger.info(settings)


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/ping", response_model=MessageResponse)
async def pong():
    return MessageResponse(data="pong!")


@app.post("/store/create", response_model=CreateStoreResponse, status_code=202)
async def create_store(
    background_tasks: BackgroundTasks,
    store_info: StoreRead,
    session: AsyncSession = Depends(get_session),
):
    """
    Receives the image and returns the url with the get info
    """

    location = store_info.location
    lat = store_info.lat
    lon = store_info.lon
    promo_code = store_info.promo_code
    logger.info(f"🛍️ POST with {lat=} {lon=} {location=} {promo_code=}")

    if promo_code != settings.PROMO_CODE:
        promo_code = None

    stores = await select_by_id(
        session, Store, [location, promo_code], ["location", "promo_code"]
    )

    try:
        stores_dict = {}
        if len(stores) == 0:
            logger.info("🛍️ No store exists - create all")
            # Fetch image from weather api first
            image_base64 = await create_image(lat=lat, lon=lon, location=location)

            for item_code in settings.PRODUCT_COLORS.keys():
                store_new = await create_store_in_db(
                    session,
                    lat,
                    lon,
                    location,
                    item_code,
                    promo_code,
                    image_base64=image_base64,
                )
                store_id = store_new.id
                logger.info(f"🛍️ Created with {store_new.id=} for {item_code=}")
                stores_dict[item_code] = store_id
                background_tasks.add_task(teemill_post_store, session, store=store_new)

        elif len(stores) > 1:
            logger.info("🛍️ Stores already exists - return ids of the ones that exist")
            for x in stores:
                stores_dict[x.Store.item_code] = x.Store.id
                if x.Store.status not in (0, 1):
                    logger.info(
                        "🛍️ Status=3 indicates something went wrong with store - "
                        f"re-create { x.Store.id=}"
                    )
                    background_tasks.add_task(
                        teemill_post_store, session, store=x.Store
                    )

    except Exception as e:
        logger.error(
            f"🔴 Something went wrong getting {stores}. {len(stores)=} {e=}. "
            "Updating to status=3"
        )
        for x in stores:
            x.Store.status = 3
        await session.commit()
        raise e

    logger.debug(stores_dict)
    return CreateStoreResponse(data=stores_dict)


@app.get("/store/status", response_model=ItemsWithColours)
async def get_store_status(
    background_tasks: BackgroundTasks,
    store_id: str = Query(default=None, min_length=1, max_length=36),
    session: AsyncSession = Depends(get_session),
):
    """
    Returns the status of the request.
    """

    store = await select_by_id(session, Store, store_id, "id")

    if len(store) == 0:
        logger.debug(f"ℹ👓 No store to return {store_id=} {store=}")
        raise HTTPException(status_code=404)

    elif len(store) == 1 and store[0].Store.status == 0:
        logger.debug("👓 Store exists but not ready")
        raise HTTPException(status_code=203)

    elif len(store) == 1 and store[0].Store.status == 3:
        logger.debug("👓 Store with error - recreate")
        background_tasks.add_task(
            teemill_post_store,
            session,
            store_id=store_id,
            image=store[0].Store.image_base64,
        )
        store[0].Store.status = 0
        await session.commit()
        raise HTTPException(status_code=203)

    else:
        # Query item info and format output
        # TODO: do only 1 query in this endpoint with a join
        item = await select_by_id(session, Item, store_id, "store_id")
        colours = await select_by_id(session, Colour, item[0].Item.id, "item_id")

        if len(colours) == 0:
            msg = f"👓 Wrong expected item and colours\n{store=}\n{item=}\n{colours=}"
            logger.error(msg)
            slack_send(msg)
            raise HTTPException(status_code=500)

        res = ItemsWithColours(
            **item[0].Item.dict(),
            item_code=store[0].Store.item_code,
            colours=[x.Colour for x in colours],
        )

        logger.debug(
            f"Returning {res.name} {res.item_code} gbp={res.gbp} eur={res.eur} "
            f"#colors={len(colours)}"
        )

        return res


@app.get("/store/image", response_model=MessageResponse)
async def get_image(
    store_id: str = Query(default=None, min_length=1, max_length=36),
    session: AsyncSession = Depends(get_session),
):
    """
    Returns the image of the location
    """

    store = await select_by_id(session, Store, store_id, "id")

    if len(store) == 0:
        logger.debug(f"ℹ👓 No store to return {store_id=} {store=}")
        raise HTTPException(status_code=203)

    else:
        return MessageResponse(data=store[0].Store.image_base64)


@app.get("/currency", response_model=CurrencyResponse)
async def get_currency(
    session: AsyncSession = Depends(get_session),
):
    gbp_to_eur, _ = await currency_conversion(session, 1)

    return CurrencyResponse(gbp_to_eur=gbp_to_eur)


@app.get("/store/image/jpg")
async def get_store_jpg(
    store_id: str = Query(default=None, min_length=1, max_length=36),
    session: AsyncSession = Depends(get_session),
):
    """
    Returns the image of the location as a jpg to be used in thumbnails
    """
    store = await select_by_id(session, Store, store_id, "id")
    if len(store) == 1:
        base64_str = store[0].Store.image_base64
        img = Image.open(
            io.BytesIO(base64.decodebytes(bytes(base64_str, "utf-8")))
        ).convert("RGB")
        imgio = io.BytesIO()
        img.save(imgio, "JPEG")
        imgio.seek(0)
        return StreamingResponse(content=imgio, media_type="image/jpeg")


@app.get("/store/random", response_model=list[StoreReadNoPromo])
async def get_store_random(
    n: Annotated[int, Path(title="The ID of the item to get", le=10)] = 10,
    session: AsyncSession = Depends(get_session),
):
    """
    Returns n random stores with basic info
    """

    results = await get_n_stores(session, n)
    return results
