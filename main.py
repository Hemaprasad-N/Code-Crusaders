from fastapi import FastAPI
from app.db_handler import init_db
from app.api import router

app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()

app.include_router(router, prefix="/api")
