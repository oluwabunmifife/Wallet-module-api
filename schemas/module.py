import datetime
from pydantic import BaseModel

class Walletbase(BaseModel):
    userID: str
    wallettype: int


class WalletCreate(Walletbase):
    pass


class Wallet(Walletbase):
    userID: str
    walletType: int
    balance: float
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    vatPercentage: float

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    amount: float
    narration: str


class TransactionCreateandUpdate(TransactionBase):
    userID: str
    transType: str
    purpose: str


class Withdraw(TransactionCreateandUpdate):
    account_number: str
    bank_name: str


class Transaction(TransactionBase):
    id: int
    userID: int
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    balanceBefore: float
    balanceAfter: float
    reference: str

    class Config:
        orm_mode = True


# class SystemTransactionBase(BaseModel):
#     amount: float
#     narration: str

# class SystemTransaction(SystemTransactionBase):
#     id: int
#     createdAt: datetime.datetime
#     updatedAt: datetime.datetime
#     balanceBefore: float
#     balanceAfter: float
#     transType: str


#     class Config:
#         orm_mode = True