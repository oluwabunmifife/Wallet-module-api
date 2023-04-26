#FastAPI imports
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

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


class TopUpWallet:
    session: Session = Depends(get_db)

    #TopUp Wallet
    @router.post('/topup')
    def topup_wallet(transaction: module.TransactionCreateandUpdate, db: Session = Depends(get_db)):
        db_wallet = crud.get_wallet(db=db, user_id=transaction.userID)
        if db_wallet is None:
            raise HTTPException(status_code=404, detail="Wallet not found")
        topup =  crud.create_transaction(db=db, transaction=transaction)
        update = crud.update_wallet_info(db=db, info_update=transaction)
        # system = crud.update_system_wallet(db=db)
        # return {
        #     "TopUp": topup,
        #     "Update": update,
        #     "System": system
        # }


        if (transaction.transType == "Debit") or (transaction.transType == "debit"):
            system = crud.update_system_wallet(db=db)
            return {
                "TopUp": topup,
                "Update": update,
                "System": system
            }
        else:
            return {
                "Update": update
            }
        

# ADD A COLUMN THAT TELLS IF A TRANSACTION WAS SUCCESSFUL OR NOT AS PER INSUFFICIENT FUNDS