from sqlalchemy import Column, BigInteger, String, Float

from app_credit.database_config.postgre_config import Base


class Debt(Base):
    __tablename__ = "debts"

    id = Column(BigInteger, primary_key=True, index=True)
    creditor = Column(String(100), nullable = False)
    debt_amount = Column(Float, nullable = False)
    interest_rate = Column(Float, nullable = False)
    # last_update = Column(Date, nullable = False)

    cpf = Column(BigInteger, nullable = False)
    # ToDo: Corrigir o relationship entre as tabelas do bd_1
    # person_id = Column(BigInteger, ForeignKey('PERSONAL_DATA.id'))
    # person_debts = relationship("Personal_Data", back_populates="debt_info", passive_deletes='all')