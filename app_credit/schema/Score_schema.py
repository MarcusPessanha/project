from typing import Dict
from pydantic import BaseModel


class Score_Info(BaseModel):
    cpf: int
    salary: float
    occupation: str
    postal_code: str
    
    # patrimony: Dict[str]
