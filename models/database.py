import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from config.db import Base
import uuid

class walletType(Base):
    __tablename__ = "walletType"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(8))
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=datetime.datetime.now)
    vatPercentage = Column(Float)

class Wallets(Base):
    __tablename__ = "wallet"
    userID = Column(String(15), primary_key=True, index=True, unique=True)
    walletType = Column(ForeignKey("walletType.id"), nullable=False, default=2)
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=datetime.datetime.now)
    balance = Column(Float)

class Transactions(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    userID = Column(ForeignKey("wallet.userID"), nullable=False)
    amount = Column(Float)
    balanceBefore = Column(Float)
    balanceAfter = Column(Float)
    narration = Column(String(35))
    transType = Column(String(15))
    purpose = Column(String(20))
    #reference = Column(String, uuid.uuid4())
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=datetime.datetime.now)
    wallet = relationship("Wallets")


class SystemTransactions(Base):
    __tablename__ = "systemTransactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    balanceBefore = Column(Float)
    balanceAfter = Column(Float)
    narration = Column(String(35))
    transType = Column(String(15))
    purpose = Column(String(20))
    createdAt = Column(DateTime, default=datetime.datetime.now)
    updatedAt = Column(DateTime, default=datetime.datetime.now)
    