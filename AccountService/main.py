import uvicorn
from fastapi import FastAPI
import settings
from core.accounts import schemas
from core.accounts.models import Account
from typing import List


app = FastAPI()

try:
    settings.create_db_connection(app)
except Exception:
    print("Failed to create database connection")


@app.post('/', response_model=schemas.AccountOutSchema)
async def register_user(request: schemas.AccountCreateSchema):
    obj = await Account.create(**request.dict())
    return obj


@app.get('/', response_model=schemas.AccountOutSchema)
async def register_user(request: schemas.AccountCreateSchema):
    print(request.dict())
    obj = await Account.create(**request.dict())
    return obj


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)