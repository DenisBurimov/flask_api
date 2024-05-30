from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from .review import ReviewGetOutput


class ProductGetInput(BaseModel):
    id: int


class ProductGetOutput(BaseModel):
    asin: str
    title: str
    reviews: list[ReviewGetOutput]

    model_config = SettingsConfigDict(from_attributes=True)
