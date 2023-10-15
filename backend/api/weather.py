import base64
import io
import textwrap
from collections import defaultdict

import aiohttp
import matplotlib as mpl
import matplotlib.pyplot as plt
from loguru import logger
from matplotlib.colors import ListedColormap

from api.models import Store
from api.utils import slack_send


def split_location(x: str, width: int = 20):
    wrapper = textwrap.TextWrapper(width=width)
    word_list = wrapper.wrap(text=x)
    return "\n".join(word_list)


async def define_jpg_image(year: list[int], temp: list[float], location: str) -> str:
    fig, ax = plt.subplots(figsize=(13.33, 7.5), dpi=96)

    # Colours - Choose the colour map - 8 blues and 8 reds
    cmap = ListedColormap(
        [
            "#08306b",
            "#08519c",
            "#2171b5",
            "#4292c6",
            "#6baed6",
            "#9ecae1",
            "#c6dbef",
            "#deebf7",
            "#fee0d2",
            "#fcbba1",
            "#fc9272",
            "#fb6a4a",
            "#ef3b2c",
            "#cb181d",
            "#a50f15",
            "#67000d",
        ]
    )

    # linearly normalizes data into the [0.0, 1.0] interval
    norm = mpl.colors.Normalize(min(temp), max(temp))

    # Plot bars
    ax.bar(year, 1, color=cmap(norm(temp)), width=1, zorder=2)

    # Remove the spines
    ax.spines[["top", "left", "bottom", "right"]].set_visible(False)

    # Reformat x-axis label and tick labels
    ax.set_xlabel("", fontsize=12, labelpad=10)
    ax.set_xticks([])
    ax.set_xlim([year[0] - 1, year[-1] + 1])

    # Reformat y-axis label and tick labels
    ax.set_ylabel("", fontsize=12, labelpad=10)
    ax.set_yticks([])
    ax.set_ylim([0, 1])

    # Set source text
    ax.text(
        x=0.3,
        y=0.15,
        s=split_location(location),
        transform=fig.transFigure,
        horizontalalignment="left",
        verticalalignment="top",
        fontsize=50,
        alpha=1,
        wrap=True,
    )

    ax.text(
        x=0.13,
        y=0.14,
        s=year[0],
        transform=fig.transFigure,
        ha="left",
        fontsize=30,
        alpha=0.7,
    )
    ax.text(
        x=0.9,
        y=0.14,
        s=year[-1],
        transform=fig.transFigure,
        ha="right",
        fontsize=30,
        alpha=0.7,
    )

    # Adjust the margins around the plot area
    plt.subplots_adjust(
        left=None, right=None, top=None, bottom=0.2, wspace=None, hspace=None
    )

    my_stringIObytes = io.BytesIO()
    fig.savefig(my_stringIObytes, format="png", transparent=True, bbox_inches="tight")
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()

    return my_base64_jpgData


async def group_by_year(years: list, temps: list) -> tuple[list, list]:
    # group by year
    data_grouped = defaultdict(list)
    for y, t in zip(years, temps):
        data_grouped[y].append(t)

    # Aggregate
    year, temp = [], []
    for y, values in data_grouped.items():
        x_tmp = [x for x in values if x]
        year.append(y)
        temp.append(sum(x_tmp) / len(x_tmp))

    # Skip last year data
    return year[:-1], temp[:-1]


async def fetch_weather_data(lat: float, lon: float) -> tuple[list[int], list[float]]:
    METEO_URL = (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}"
        f"&longitude={lon}"
        "&start_date=1940-01-01&end_date=2023-05-08&models=best_match"
        "&daily=temperature_2m_mean&timezone=Europe%2FBerlin"
    )

    async with aiohttp.ClientSession() as aio_session:
        async with aio_session.get(METEO_URL, timeout=200) as response:
            if response.status == 200:
                # Save to DB
                logger.info("🟢 🤟 200 response -> Process meteo data and save")
                data = await response.json()
                raw_year = [int(x[:4]) for x in data["daily"]["time"]]
                raw_temp = data["daily"]["temperature_2m_mean"]
                year, temp = await group_by_year(years=raw_year, temps=raw_temp)

                return year, temp

            else:
                msg = f"🔴 {response=}"
                logger.error(msg)
                slack_send(msg)
                response.raise_for_status()


async def create_image(lat: float, lon: float, location: str) -> Store:
    """Fetches weather image from a store"""

    year, temp = await fetch_weather_data(lat=lat, lon=lon)
    image = await define_jpg_image(year=year, temp=temp, location=location)

    return image
