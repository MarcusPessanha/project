from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, MetaData, Table, Column
from sqlalchemy.orm import relationship

from .database import Base

class Personal_Data(Base):
    __tablename__ = "PERSONAL_DATA"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(Integer, unique=True)
    name = Column(String(100))
    surname = Column(String(100))
    age = Column(Integer)
    creditcard_id = Column(Integer)
    phone = Column(Integer)

    person_id = Column(Integer, ForeignKey('ADDRESS_DATA.id'))
    address_info = relationship("Address_Data", back_populates="address_data")


class Address_Data(Base):
    __tablename__ = "ADDRESS_DATA"

    id = Column(Integer, primary_key=True, index=True)
    postal_code = Column(Integer)
    street = Column(String(100))
    district = Column(String(100))
    city_id = Column(String(100))
    country = Column(String(100))
    last_update = Column(String(100))

    address_data = relationship("Personal_Data", back_populates="address_info")


class User(Base):
    __tablename__ = "APP_USERS"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(100))
    email = Column(String(100))
    cpf = Column(Integer, unique=True)  
    password = Column(String)


    # patrimony = Column(String(100))
    # address_cep = Column(Integer)
    # occupation = Column(String(100))


# class Debt_Data(Base):
#     __tablename__ = "DEBT_DATA"

#     debt_id = Column(Integer, primary_key=True, index=True)
#     creditor = Column(String(100))
#     debt_amount = Column(Float)
#     interest = Column(Float)