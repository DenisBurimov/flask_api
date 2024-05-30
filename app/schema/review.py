from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class ReviewGetOutput(BaseModel):
    product_id: int
    title: str
    review: str

    model_config = SettingsConfigDict(from_attributes=True)
