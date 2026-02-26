from fastapi import FastAPI
from routers.company_router import router as company_router
from routers.auth_router import router as auth_router
from db import engine, Base

app = FastAPI()  # sempre criar app primeiro !!

Base.metadata.create_all(bind=engine)

app.include_router(company_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return {"status": "ContaAI rodando"}