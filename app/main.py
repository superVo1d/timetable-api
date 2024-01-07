from fastapi import FastAPI

from app.api import index

app = FastAPI()

app.include_router(index.router, prefix="")
