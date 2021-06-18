from sqlalchemy import Column, Integer, BigInteger, String
from app_credit.database_config.postgre_config import Base


class Personal(Base):
    __tablename__ = "personals"

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