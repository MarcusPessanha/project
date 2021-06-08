from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, MetaData, Table, Column
from sqlalchemy.orm import relationship

from .database import Base

class Base_A(Base):
    __tablename__ = "SENSITIVE_DATA"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(Integer, unique=True)
    name = Column(String(100))
    address_cep = Column(Integer)
    debt_list = Column(Float)

    person_id = Column(Integer, ForeignKey('SCORE_DATA.id'))
    sensitive_data = relationship("Base_B", back_populates="score_data")


class Base_B(Base):
    __tablename__ = "SCORE_DATA"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    patrimony = Column(String(100))
    address_cep = Column(Integer)
    occupation = Column(String(100))
    
    score_data = relationship("Base_A", back_populates="sensitive_data")


class User(Base):
    __tablename__ = "APP_USERS"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(100))
    email = Column(String(100))
    cpf = Column(Integer, unique=True)  
    password = Column(String)

