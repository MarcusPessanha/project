from pydantic import BaseModel


class Personal_Info(BaseModel):
    cpf: int
    name: str
    surname: str
    age: int
    creditcard_id: int
    phone: int

    class Config:
        orm_mode = True


