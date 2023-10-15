from datetime import datetime, timedelta

import aiohttp
from forex_python.converter import CurrencyRates
from loguru import logger
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.models import Currency
from api.utils import slack_send


def get_rates_fallback() -> tuple[float, float]:
    """Convert from gbp to eur and usd"""
    c = CurrencyRates()
    try:
        gbp_to_eur = c.get_rate("GBP", "EUR")
        gbp_to_usd = c.get_rate("GBP", "USD")
    except Exception as e:
        # Fallback
        logger.error(e)
        slack_send(e)
        gbp_to_eur = 1.16
        gbp_to_usd = 1.25
    return gbp_to_eur, gbp_to_usd


async def get_rates():
    """Rates from European Exchange. See https://data.ecb.europa.eu/help/api/data
    and https://data.ecb.europa.eu/currency-converter"""

    async with aiohttp.ClientSession() as aio_session:
        params = {
            "lastNObservations": "1",
            "detail": "dataonly",
            "format": "jsondata",
        }
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        url = "https://data-api.ecb.europa.eu/service/data/EXR/D.USD+GBP.EUR.SP00.A"

        async with aio_session.get(
            url, params=params, headers=headers, timeout=300
        ) as response:
            if response.status == 200:
                data = await response.json()

                # Extract the latest exchange rate
                order = [
                    x["values"]
                    for x in data["structure"]["dimensions"]["series"]
                    if x["id"] == "CURRENCY"
                ][0]
                if order[0]["id"] == "GBP":
                    id_gbp, id_usd = 0, 1
                else:
                    id_gbp, id_usd = 1, 0
                eur_to_gbp = data["dataSets"][0]["series"][f"0:{id_gbp}:0:0:0"][
                    "observations"
                ]["0"][0]
                eur_to_usd = data["dataSets"][0]["series"][f"0:{id_usd}:0:0:0"][
                    "observations"
                ]["0"][0]

            else:
                logger.error(
                    f"Failed to retrieve data. Status code: {response.status_code}"
                )

            gbp_to_eur = 1 / eur_to_gbp
            usd_to_eur = 1 / eur_to_usd
            gbp_to_usd = gbp_to_eur * (1 / usd_to_eur)

            return gbp_to_eur, gbp_to_usd


async def currency_conversion(session: AsyncSession, gbp: float) -> tuple[float, float]:
    """Convert from gbp to eur and usd, only if the last update was more than
    1 day ago"""

    # Fetch Currency table
    currency_results = await session.execute(select(Currency))
    currency_item = currency_results.first()[0]
    diff_last_update = datetime.now() - currency_item.modified
    gbp_to_eur = currency_item.gbp_to_eur
    gbp_to_usd = currency_item.gbp_to_usd

    logger.info(f"Last update of currency: {diff_last_update}")
    logger.info(datetime.now())
    if diff_last_update > timedelta(days=1):
        # Update rates
        logger.debug(f"Updating currency rates: {diff_last_update=}")
        try:
            gbp_to_eur, gbp_to_usd = await get_rates()
            # Update db
            currency_item.gbp_to_eur = gbp_to_eur
            currency_item.gbp_to_usd = gbp_to_usd
            currency_item.modified = datetime.now()
            await session.commit()

        except Exception as e:
            logger.exception(e)
            # Use existing ones for fallback
            gbp_to_eur, gbp_to_usd = get_rates_fallback()

    return gbp_to_eur * gbp, gbp_to_usd * gbp
