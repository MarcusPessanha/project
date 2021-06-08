from pydantic import BaseModel
from typing import Optional


class Person(BaseModel):
    cpf: int
    name: str
    address_cep: int
    debt_list: Optional[float] = None
    age: int
    patrimony: str
    occupation: str

    person_id = str


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