from fastapi import HTTPException
from sqlalchemy.orm import Session
import random

from models import database
from schemas import module


def get_wallet(db: Session, user_id: str):
    wallet_info = db.query(database.Wallets).get(user_id)

    if wallet_info is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet_info

def get_wallets(db: Session, skip: int = 0, limit: int = 50):
    return db.query(database.Wallets).offset(skip).limit(limit).all()


def create_wallet(wallet: module.WalletCreate, db: Session):
    balance =  random.randint(100, 1000)
    db_wallet = database.Wallets(userID=wallet.userID, walletType=wallet.wallettype, balance=balance)
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

def get_transaction(db: Session, user_id: str):
    return db.query(database.Transactions).filter(database.Transactions.userID == user_id).first()

def get_transactions(db: Session, skip: int = 0, limit: int = 50):
    return db.query(database.Transactions).offset(skip).limit(limit).all()

def create_transaction(db: Session, transaction: module.TransactionCreateandUpdate):
    #IF TRANSACTION TYPE IS DEBIT
    if (transaction.transType == "Debit") or (transaction.transType == "debit"):

        #QUERY THE DATABASE TABLE
        balanceBefore = db.query(database.Wallets).filter(database.Wallets.userID == transaction.userID).first().balance
        #CHECK IF BALANCE IS LESS THAN TRANSACTION AMOUNT
        if balanceBefore < transaction.amount:
            raise HTTPException(status_code=404, detail="Insufficient Funds")
        #IF BALANCE IS MORE THAN TRANSACTION AMOUNT, THEN CONTINUE ---->>>>>>>>>>>>>>>>>>>>>
        
        #UPDATING SYSTEM WALLET
        try:
            sysBalanceBefore = db.query(database.Wallets).filter(database.Wallets.userID == "system").first().balance
        except AttributeError:
            sysBalanceBefore = 0
        sysBalanceAfter = sysBalanceBefore + transaction.amount

        #SYSTEM TRANSACTION UPDATE
        sys_transaction = database.SystemTransactions(amount=transaction.amount, narration=transaction.narration, transType="Credit", purpose=transaction.purpose, balanceBefore=sysBalanceBefore, balanceAfter=sysBalanceAfter)

        #PERFORM WALLET DEBIT
        transaction.amount = -transaction.amount
        balanceAfter = balanceBefore + transaction.amount
        db_transaction = database.Transactions(amount=transaction.amount, 
                                           narration=transaction.narration, userID=transaction.userID, 
                                           transType=transaction.transType, purpose=transaction.purpose, balanceBefore=balanceBefore, balanceAfter=balanceAfter)
        db.add_all([db_transaction, sys_transaction])
        db.commit()
        db.refresh(db_transaction)
        db.refresh(sys_transaction)
        return db_transaction

       
    if (transaction.transType == "Credit") or (transaction.transType == "credit"):
        #IF TRANSACTION TYPE IS CREDIT
        balanceBefore = db.query(database.Wallets).filter(database.Wallets.userID == transaction.userID).first().balance
        balanceAfter = balanceBefore + transaction.amount
        db_transaction = database.Transactions(amount=transaction.amount, 
                                            narration=transaction.narration, userID=transaction.userID, 
                                            transType=transaction.transType, purpose=transaction.purpose, balanceBefore=balanceBefore, balanceAfter=balanceAfter)
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    
    # if (transaction.transType != "Debit") or (transaction.transType != "debit") or (transaction.transType != "Credit") or (transaction.transType != "credit"):
    #     return "Invalid transaction type"



def update_wallet_info(db: Session, info_update: module.TransactionCreateandUpdate):
    #GET WALLET BY USER ID
    find_wallet = get_wallet(db, info_update.userID)

    if find_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    #ORDER TABLE BY ID (DESCENDING) AND GET THE FIRST ROW (LATEST TRANSACTION)
    check_table = db.query(database.Transactions).order_by(database.Transactions.id.desc()).filter(database.Transactions.userID == info_update.userID).first().balanceAfter
    find_wallet.balance = check_table
    db.commit()
    db.refresh(find_wallet)
    return find_wallet

def update_system_wallet(db: Session):
    check_table = db.query(database.SystemTransactions).order_by(database.SystemTransactions.id.desc()).first().balanceAfter
    sys_wallet = get_wallet(db, "system")
    sys_wallet.balance = check_table
    db.commit()
    db.refresh(sys_wallet)

def withdraw(db: Session, transaction: module.Withdraw):
    if (transaction.transType == "Credit") or (transaction.transType == "credit"):
        return("Invalid Transaction Type. Try again")
    
    if (transaction.transType == "Debit") or (transaction.transType == "debit"):
        #QUERY THE DATABASE TABLE
        balanceBefore = db.query(database.Wallets).filter(database.Wallets.userID == transaction.userID).first().balance
        #CHECK IF BALANCE IS LESS THAN TRANSACTION AMOUNT
        if balanceBefore < transaction.amount:
            raise HTTPException(status_code=404, detail="Insufficient Funds")
        #IF BALANCE IS MORE THAN TRANSACTION AMOUNT, THEN CONTINUE ---->>>>>>>>>>>>>>>>>>>>>


        #PERFORM WALLET DEBIT
        transaction.amount = -transaction.amount
        balanceAfter = balanceBefore + transaction.amount
        db_transaction = database.Transactions(amount=transaction.amount, 
                                           narration=transaction.narration, userID=transaction.userID, 
                                           transType=transaction.transType, purpose=transaction.purpose, balanceBefore=balanceBefore, balanceAfter=balanceAfter)
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return {
            "Funds successfully withdrawn", 
            db_transaction
        }
    

def send(db: Session, transaction: module.Send):
    if (transaction.transType == "Credit") or (transaction.transType == "credit"):
        return("Invalid Transaction Type. Try again")
    
    if (transaction.transType == "Debit") or (transaction.transType == "debit"):
        #QUERY THE DATABASE TABLE
        balanceBefore = db.query(database.Wallets).filter(database.Wallets.userID == transaction.userID).first().balance
        #CHECK IF BALANCE IS LESS THAN TRANSACTION AMOUNT
        if balanceBefore < transaction.amount:
            raise HTTPException(status_code=404, detail="Insufficient Funds")
        #IF BALANCE IS MORE THAN TRANSACTION AMOUNT, THEN CONTINUE ---->>>>>>>>>>>>>>>>>>>>>

        receiveid = db.query(database.Wallets).filter(database.Wallets.userID == transaction.receiverID).first()
        receiverbalance = receiveid.balance

        #CREDIT RECEIVER
        newreceiverbalance = receiverbalance + transaction.amount
        db_transaction2 = database.Transactions(amount=transaction.amount, 
                                            narration=transaction.narration, userID=transaction.receiverID, 
                                            transType=transaction.transType, purpose=transaction.purpose, balanceBefore=receiverbalance, balanceAfter=newreceiverbalance)

        #PERFORM WALLET DEBIT
        transaction.amount = -transaction.amount
        balanceAfter = balanceBefore + transaction.amount
        db_transaction1 = database.Transactions(amount=transaction.amount, 
                                           narration=transaction.narration, userID=transaction.userID, 
                                           transType=transaction.transType, purpose=transaction.purpose, balanceBefore=balanceBefore, balanceAfter=balanceAfter)
        
        db.add_all([db_transaction1, db_transaction2])
        db.commit()
        db.refresh(db_transaction1)
        db.refresh(db_transaction2)
        return db_transaction1, db_transaction2
    
def update_receiver_info(db: Session, info_update: module.Send):
    #GET WALLET BY RECEIVER ID
    find_wallet = get_wallet(db, info_update.receiverID)

    if find_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    #ORDER TABLE BY ID (DESCENDING) AND GET THE FIRST ROW (LATEST TRANSACTION)
    check_table = db.query(database.Transactions).order_by(database.Transactions.id.desc()).filter(database.Transactions.userID == info_update.receiverID).first().balanceAfter
    find_wallet.balance = check_table
    db.commit()
    db.refresh(find_wallet)
    return find_wallet