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

# url = "https://api.paystack.co/bank?currency=NGN"

# @router.get('/get_banks')
# def get_banks():
#     response =requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print('Error:', response.status_code, response.content)
    

# @router.post('/create_recipient')
# def create_recipient(request: module.WithdrawCreate):
        
        

#         response = TransferRecipient.create(
#         type='nuban',
#         name=request.reciepient_name,
#         account_number=request.account_number,
#         bank_code=request.bank_code,
#         currency='NGN'
#     )
        
#         if response['status']:
             
#             # Recipient creation is successful
#             # Perform necessary actions (e.g., store recipient ID, update database, etc.)
#             recipient_id = response['data']['recipient_code']
#             return {'recipient_id': recipient_id}
#         else:
#             # Recipient creation failed
#             print(response['status'])
#             return {'message': 'Recipient creation failed'}


@router.post('/withdraw')
def withdraw(transaction: module.TransactionCreateandUpdate, db: Session = Depends(get_db)):
    db_wallet = crud.get_wallet(db=db, user_id=transaction.userID)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    withdraw = crud.withdraw(db=db, transaction=transaction)
    update = crud.update_wallet_info(db=db, info_update=transaction)

    return "Your funds have been successfully withdrawn."