from fastapi import FastAPI
from routes import createWallet, index, viewwallet, topup, withdraw
from config.db import engine, SessionLocal
from models import database

app = FastAPI()

database.Base.metadata.create_all(bind=engine)


app.include_router(createWallet.router)
app.include_router(index.router)
app.include_router(viewwallet.router)
app.include_router(topup.router)
app.include_router(withdraw.router)




