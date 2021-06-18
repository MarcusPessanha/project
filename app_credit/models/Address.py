from sqlalchemy import Column, Integer, BigInteger, String, Date

from app_credit.database_config.postgre_config import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    postal_code = Column(BigInteger, nullable=False)
    number = Column(Integer, nullable=False)
    street = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    city_id = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    last_update = Column(Date, nullable=False)

    cpf = Column(BigInteger, unique=True, nullable = False)
    # ToDo: Corrigir o relationship entre as tabelas do bd_1
    # person_id = Column(BigInteger, ForeignKey('PERSONAL_DATA.id'))
    # person_address = relationship("Personal_Data", back_populates="address_info", passive_deletes='all')