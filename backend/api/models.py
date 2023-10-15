import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Event(SQLModel, table=True):
    class Config:
        extra = "ignore"
        validate_assignment = True

    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    type: Optional[str]
    origin: Optional[str]
    data: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MessageResponse(BaseModel):
    """Empty response"""

    data: Optional[str]


class CreateStoreResponse(BaseModel):
    """Response model for store/create"""

    data: dict[str, str]


class ItemBaseRead(SQLModel):
    name: Optional[str]
    url: Optional[str]  # Url of the shop
    main_image: Optional[str]
    gbp: Optional[float]
    eur: Optional[float]
    usd: Optional[float]


class ItemBase(ItemBaseRead):
    external_id: Optional[str]  # Teemill id
    store_id: Optional[str] = Field(
        default=None, foreign_key="store.id"
    )  # My own reference
    created: datetime = Field(default_factory=datetime.utcnow)
    modified: datetime = Field(default_factory=datetime.utcnow)


class Item(ItemBase, table=True):
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)


class ItemRead(ItemBase):
    id: Optional[str]


class StoreReadNoPromo(SQLModel):
    location: str
    lat: float
    lon: float


class StoreRead(StoreReadNoPromo):
    promo_code: Optional[str]


class Store(StoreRead, table=True):
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    status: Optional[int]  # 0: pending 1: ready 2: cancelled
    name: Optional[str]
    description: Optional[str]
    image_base64: Optional[str]
    item_code: Optional[str] = "RNA1"
    colours: Optional[str]
    price: Optional[float]
    cross_sell: Optional[bool] = Field(default=True)
    created: datetime = Field(default_factory=datetime.utcnow)


class ColourBaseRead(SQLModel):
    name: Optional[str]
    url: Optional[str]


class ColourBase(ColourBaseRead):
    item_id: Optional[str] = Field(default=None, foreign_key="item.id")


class Colour(ColourBase, table=True):
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)


class ItemsWithColours(ItemBaseRead):
    item_code: str
    colours: list[ColourBaseRead] = []


class CurrencyResponse(SQLModel):
    gbp_to_eur: Optional[float]


class Currency(CurrencyResponse, table=True):
    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    modified: Optional[datetime]
    gbp_to_usd: Optional[float]
