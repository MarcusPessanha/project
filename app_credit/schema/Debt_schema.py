from typing import Optional

from pydantic import BaseModel


class Debt_Info(BaseModel):
    creditor: Optional[str]
    debt_amount: Optional[float]
    interest_rate: Optional[float]

    class Config:
        orm_mode = True


class Debt_In(BaseModel):
    cpf: int
    creditor: str
    debt_amount: float
    interest_rate: float


class Debt_Update(BaseModel):
    creditor: Optional[str]
    debt_amount: Optional[float]
    interest_rate: Optional[float]