from typing import Optional

import aiohttp
from loguru import logger
from sqlmodel.ext.asyncio.session import AsyncSession

from api.currency import currency_conversion
from api.models import Colour, Item, Store
from api.settings import settings
from api.utils import slack_send


async def create_store_in_db(
    session: AsyncSession,
    lat: float,
    lon: float,
    location: str,
    item_code: str,
    promo_code: Optional[str],
    image_base64: Optional[str],
) -> Store:
    """Creates an entry in the store table and return id"""

    if promo_code:
        price = 0
    else:
        price = settings.PRODUCT_COLORS[item_code]["price"]
    store = Store(
        status=0,
        lat=lat,
        lon=lon,
        location=location,
        name=f"#ShowYourLocalStripes at {location}",
        description=f"#ShowYourLocalStripes at {location}",
        item_code=item_code,
        colours=settings.PRODUCT_COLORS[item_code]["colours"],
        price=price,
        image_base64=image_base64,
        cross_sell=True,
        promo_code=promo_code,
    )
    logger.info(
        f"🏬 Creating an empty store: {store.id=} {store.location=} {store.item_code=}"
    )
    session.add(store)
    await session.commit()

    return store


async def teemill_post_store(session: AsyncSession, store: Store) -> None:
    async with aiohttp.ClientSession() as aio_session:
        payload = {
            "image_url": "data:image/png;base64," + store.image_base64,
            "item_code": store.item_code,
            "name": store.name,
            "colours": store.colours,
            "description": store.description,
            "price": store.price,
            "cross_sell": store.cross_sell,
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {settings.TEEMILL_API_KEY.get_secret_value()}",
        }

        async with aio_session.post(
            settings.TEEMILL_URL, json=payload, headers=headers, timeout=300
        ) as response:
            if response.status == 200:
                # Save to DB
                logger.info(
                    f"🟢 🤟 200 response teemill {store.id=} {store.location=} "
                    f"{store.item_code=} -> Save to DB"
                )
                body = await response.json()

                # Attempt to translate gbp to Eur and USD
                gbp = body["price"].get("gbp")
                currency = await currency_conversion(session, gbp)
                eur, usd = currency

                item_new = Item(
                    external_id=body["id"],
                    store_id=store.id,
                    name=body["name"],
                    url=body["url"],
                    main_image=body["image"],
                    gbp=gbp,
                    eur=eur,
                    usd=usd,
                )
                session.add(item_new)
                await session.commit()

                for name, url in body["colours"].items():
                    colour_new = Colour(item_id=item_new.id, name=name, url=url)
                    session.add(colour_new)

                store.status = 1
                await session.commit()

            else:
                logger.error(f"🔴 {response=}")
                store.status = 3
                msg = f"🔴 Updating store status =3 for  {store.id=}"
                logger.error(msg)
                slack_send(msg)
                await session.commit()
