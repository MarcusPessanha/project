from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    postal_code: int
    street: str
    district: str
    city_id: str
    country: str
    last_update: str

class Person(BaseModel):
    cpf: int
    name: str
    surname: str
    age: str
    creditcard_id: int
    phone: int

    postal_code: int
    street: str
    district: str
    city_id: str
    country: str
    last_update: str

    # debt_list: Optional[float] = None

    person_id: int
    # address_info = Address


class Person_View(BaseModel):
    cpf: int
    name: str
    surname: str
    age: str
    creditcard_id: int
    phone: int

    address_info: Address

    class Config:
        orm_mode = True


class User(BaseModel):
    login: str
    email: str
    cpf: int
    password: str


class User_View(BaseModel):
    login: str
    email: str
    cpf: int
    
    class Config:
        orm_mode = True