from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import date, datetime


class Redis_Query(BaseModel):
    cpf: int
    bureau_postal_code: int


class Redis_Purchase(BaseModel):
    cpf: int
    creditcard_id: int
    store: str
    store_postal_code: int
    value: float
