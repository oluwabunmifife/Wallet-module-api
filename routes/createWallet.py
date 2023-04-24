#FastAPI imports
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

#Submodules
from config import crud
from models import database
from schemas import module
from config.db import SessionLocal, engine
#from main import get_db


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/create", status_code=201)
def new_wallet(wallet: module.WalletCreate, db: Session = Depends(get_db)):
    check = db.query(database.Wallets).filter(database.Wallets.userID == wallet.userID).first()
    if check:
        raise HTTPException(status_code=400, detail="Wallet already exists")
    return crud.create_wallet(wallet=wallet, db=db)
    
