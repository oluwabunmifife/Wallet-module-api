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


@router.get("/view")
def get_wallets(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    db_wallet = crud.get_wallets(db, skip=skip, limit=limit)
    return db_wallet

@router.get("/view/{user_id}")
def get_wallet(user_id: str, db: Session = Depends(get_db)):
    db_wallet = crud.get_wallet(db, user_id=user_id)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return db_wallet