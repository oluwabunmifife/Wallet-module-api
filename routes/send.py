#FastAPI imports
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
# from paystackapi.trecipient import TransferRecipient
# from paystackapi.paystack import Paystack
import requests

#Submodules
from config import crud
from models import database
from schemas import module
from config.db import SessionLocal, engine


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/send')
def send_money(transaction: module.Send, db: Session = Depends(get_db)):
    sender_wallet = crud.get_wallet(db=db, user_id=transaction.userID)
    if sender_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    receiver_wallet = crud.get_wallet(db=db, user_id=transaction.receiverID)
    if receiver_wallet is None:
         raise HTTPException(status_code=404, detail="Wallet not found")
    send = crud.send(db=db, transaction=transaction)
    update_sender = crud.update_wallet_info(db=db, info_update=transaction)
    update_receiver = crud.update_receiver_info(db=db, info_update=transaction)
    return {
        "Sender_update": update_sender,
        "Receiver_update": update_receiver
    }