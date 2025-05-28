from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class AddMoney(BaseModel):
    amount: float


class TradeAsset(BaseModel):
    symbol: str
    quantity: float

