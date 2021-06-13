from pydantic import BaseModel
from typing import Optional, List, Dict


class Personal_Info(BaseModel):
    cpf: int
    name: str
    surname: str
    age: int
    creditcard_id: int
    phone: int

    class Config:
        orm_mode = True


class Address_Info(BaseModel):
    postal_code: int
    number: int
    street: str
    district: str
    city_id: str
    country: str
    last_update: str

    class Config:
        orm_mode = True


class Debt_Info(BaseModel):
    creditor: Optional[str]
    debt_amount: Optional[float]
    interest_rate: Optional[float]

    class Config:
        orm_mode = True


class Person_In(BaseModel):
    personal_info: Personal_Info
    address_info: Address_Info
    debt_info: Optional[Debt_Info]


class Debt_In(BaseModel):
    cpf: int
    creditor: str
    debt_amount: float
    interest_rate: float

    
class Person_View(BaseModel):
    personal_info: Personal_Info
    address_info: Address_Info
    debt_info: List[Debt_Info]

    class Config:
        orm_mode = True


class Person_Update(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    age: Optional[int]
    creditcard_id: Optional[int]
    phone: Optional[int]
    postal_code: Optional[int]
    street: Optional[str]
    district: Optional[str]
    city_id: Optional[str]
    country: Optional[str]
    last_update: Optional[str]


class Debt_Update(BaseModel):
    creditor: Optional[str]
    debt_amount: Optional[float]
    interest_rate: Optional[float]
    last_update: Optional[str]


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