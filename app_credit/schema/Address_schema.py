from datetime import date
from pydantic import BaseModel


class Address_Info(BaseModel):
    postal_code: int
    number: int
    street: str
    district: str
    city_id: str
    country: str

    class Config:
        orm_mode = True


class Address_View(BaseModel):
    postal_code: int
    number: int
    street: str
    district: str
    city_id: str
    country: str
    last_update: date

    class Config:
        orm_mode = True