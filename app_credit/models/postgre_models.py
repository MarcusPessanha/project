from sqlalchemy import Column, ForeignKey, Integer, BigInteger, String, Float, Column, Date
from sqlalchemy.orm import relationship
from ..database_config.postgre_config import Base

class Personal_Data(Base):
    __tablename__ = "PERSONAL_DATA"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(BigInteger, unique=True, nullable = False)
    name = Column(String(100), nullable = False)
    surname = Column(String(100), nullable = False)
    age = Column(Integer)
    creditcard_id = Column(BigInteger, unique=True)
    phone = Column(BigInteger)
    # last_update = Column(Date, nullable = False)

    # ToDo: Corrigir o relationship entre as tabelas do bd_1 
    # address_info = relationship("Address_Data", back_populates="person_address", cascade="all, delete" )
    # debt_info = relationship("Debt_Data", back_populates="person_debts", cascade="all, delete")


class Address_Data(Base):
    __tablename__ = "ADDRESS_DATA"

    id = Column(Integer, primary_key=True, index=True)
    postal_code = Column(BigInteger, nullable = False)
    number = Column(Integer, nullable = False)
    street = Column(String(100), nullable = False)
    district = Column(String(100), nullable = False)
    city_id = Column(String(100), nullable = False)
    country = Column(String(100), nullable = False)
    last_update = Column(Date, nullable = False)

    cpf = Column(BigInteger, unique=True, nullable = False)
    # ToDo: Corrigir o relationship entre as tabelas do bd_1 
    # person_id = Column(BigInteger, ForeignKey('PERSONAL_DATA.id'))
    # person_address = relationship("Personal_Data", back_populates="address_info", passive_deletes='all')


class Debt_Data(Base):
    __tablename__ = "DEBT_DATA"

    id = Column(BigInteger, primary_key=True, index=True)
    creditor = Column(String(100), nullable = False)
    debt_amount = Column(Float, nullable = False)
    interest_rate = Column(Float, nullable = False)
    # last_update = Column(Date, nullable = False)

    cpf = Column(BigInteger, nullable = False)
    # ToDo: Corrigir o relationship entre as tabelas do bd_1 
    # person_id = Column(BigInteger, ForeignKey('PERSONAL_DATA.id'))
    # person_debts = relationship("Personal_Data", back_populates="debt_info", passive_deletes='all')


class User(Base):
    __tablename__ = "APP_USERS"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(100))
    email = Column(String(100))
    cpf = Column(BigInteger, unique=True)  
    password = Column(String)
