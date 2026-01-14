from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import List


# class output_permanent(Base):
#     description = Column(String)
#     category = Column(String)
#     value = Column(Float)
#     bank = Column(String)
#     init_date = Column(Date)
#     end_date = Column(Date)
#     rate = Column(Float)
#     is_delete = Column(Integer, default=0)

# class output_hist(Base):
#     __tablename__ = "output_hist"

#     pk_oh = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     category = Column(String)
#     value = Column(Float)
#     date = Column(Date)
#     is_delete = Column(Integer, default=0)


# class input_permanent(Base):
#     __tablename__ = "input_permanent"

#     pk_ip = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     description = Column(String)
#     value = Column(Float)
#     bank = Column(String)
#     is_delete = Column(Integer, default=0)


# class input_hist(Base):
#     __tablename__ = "input_hist"

#     pk_ih = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     description = Column(String)
#     value = Column(Float)
#     date = Column(Date)
#     bank = Column(String)
#     is_delete = Column(Integer, default=0)


# class purchases_installments(Base):
#     __tablename__ = "purchases_installments"

#     pk_purch = Column(Integer, primary_key=True, index=True)
#     fk_oh = Column(Integer, ForeignKey("output_hist.pk_oh"), nullable=False)
#     value = Column(Float)
#     category = Column(String)
#     installments = Column(Integer)
#     date = Column(Date)
#     p_month = Column(Date)
#     bank = Column(String)
#     payment_method = Column(String)
#     localization = Column(String)
#     who = Column(String)
#     is_delete = Column(Integer, default=0)

#     historico = relationship("output_hist", backref="purchases_installments")


# class purchase_itens(Base):
#     __tablename__ = "purchase_itens"

#     pk_pi = Column(Integer, primary_key=True, index=True)
#     fk_purch_inst = Column(Integer, nullable=False)
#     description = Column(String)
#     value = Column(Float)
#     is_delete = Column(Integer, default=0)


# Buying schemas
class BuyingItensBase(BaseModel):
    description: str
    value: float

class BuyingInstallmentsCreate(BaseModel):
    installments: int
    itens: List[BuyingItensBase]
    bank: str
    location: str
    who: str

class BuyingItensResponse(BuyingItensBase):
    pk_pi: int # O Dashboard precisa do ID para filtros e edições
    fk_purch_inst: int
    
    # A LINHA MÁGICA: Colocamos aqui porque este schema lê do banco
    model_config = ConfigDict(from_attributes=True)

class BuyingInstallmentsResponse(BuyingInstallmentsCreate):
    pk_purch: int
    fk_oh: int
    value: float
    date: str
    p_month: str
    category: str
    payment_method: str

    model_config = ConfigDict(from_attributes=True)


# Bank schemas
class BankBase(BaseModel):
    name: str
    due_date: int

class BankCreate(BankBase):
    pass

class BankResponse(BankBase):
    pk_bk: int # O Dashboard precisa do ID para filtros e edições
    
    # A LINHA MÁGICA: Colocamos aqui porque este schema lê do banco
    model_config = ConfigDict(from_attributes=True)
