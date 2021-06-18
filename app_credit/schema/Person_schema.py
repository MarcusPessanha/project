from typing import Optional, List
from pydantic import BaseModel
from app_credit.schema.Address_schema import Address_Info, Address_View
from app_credit.schema.Personal_schema import Personal_Info
from app_credit.schema.Debt_schema import Debt_Info


class Person_In(BaseModel):
    personal_info: Personal_Info
    address_info: Address_Info
    debt_info: Optional[Debt_Info]


class Person_View(BaseModel):
    personal_info: Personal_Info
    address_info: Address_View
    debt_info: List[Debt_Info]

    class Config:
        orm_mode = True


class Person_Update(BaseModel):
    name: str
    surname: str
    age: int
    creditcard_id: int
    phone: int
    postal_code: int
    street: str
    district: str
    city_id: str
    country: str