from sqlalchemy import Integer, BigInteger, String, Column
from ..database_config.postgre_config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(100))
    email = Column(String(100))
    cpf = Column(BigInteger, unique=True)  
    password = Column(String)
