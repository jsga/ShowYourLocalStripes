from typing import Dict, Optional, Union

from dotenv import find_dotenv
from pydantic import BaseSettings, SecretStr, root_validator


class Settings(BaseSettings):
    DB_USER: Optional[str] = "climate"
    DB_PASS: SecretStr = "climate"
    DB_HOST: str = "0.0.0.0"
    DB_PORT: Union[int, str] = "5432"
    DB_NAME: str = "climatedb"
    SSL: bool = True

    ASYNC_DB_URI: Optional[SecretStr]
    SYNC_DB_URI: Optional[SecretStr]
    TEST_DB_URI: str = "postgresql+asyncpg://climate:climate@db/climatedb"
    TEEMILL_API_KEY: SecretStr = "TEEMILL_API_KEY"
    TEEMILL_URL: str = "https://teemill.com/omnis/v3/product/create"
    DEFAULT_PRICE: int = 50
    PROMO_CODE: str = "xxx"
    SLACK_TOKEN: SecretStr = "xxx"
    OPEN_METEO_KEY: SecretStr = "xxx"
    PRODUCT_COLORS = {
        # Mens tshirt
        "RNA1": {
            "colours": (
                "White,Black,Navy Blue,Athletic Grey,Denim Blue,Dark Grey,"
                "Mustard,Red,Bright Blue"
            ),
            "price": 20,
        },
        # Mens hoodie
        "RNA7": {
            "colours": "Stone Blue, Rust, White, Black, Navy, Light Heather",
            "price": 43,
        },
        # Tote bag
        "RNT1": {"colours": "Natural, White, Black", "price": 15},
        # Women's Pullover Hoody
        "RNB13": {
            "colours": "Stone Blue, Mauve, Black, Navy Blue, Light Heather",
            "price": 43,
        },
        # Women's Plain T-shirt
        "RNB46": {"colours": "White, Stone Blue", "price": 20},
        # Women's Crew Neck T-shirt
        "RNB14": {
            "colours": (
                "Pastel Green, Stone Blue,Mauve,Cherry,Mustard,Khaki,Pink,"
                "Athletic Grey,White"
            ),
            "price": 20,
        },
    }

    @root_validator
    def define_uris(cls, values) -> Dict:
        url = (
            f"{values['DB_USER']}:{values['DB_PASS'].get_secret_value()}@"
            f"{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        )

        if values["SSL"]:
            url += "?ssl=allow"
        values["ASYNC_DB_URI"] = SecretStr(f"postgresql+asyncpg://{url}")
        values["SYNC_DB_URI"] = SecretStr(f"postgresql://{url}")

        return values

    class Config:
        case_sensitive = True
        _env_file = find_dotenv()


settings = Settings()
