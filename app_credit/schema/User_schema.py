from pydantic import BaseModel


class User_Schema(BaseModel):
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