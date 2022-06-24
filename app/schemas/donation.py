from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt

from app.schemas.base import CharityBase


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str] = None

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationUser(DonationCreate):

    id: int
    create_date: dt

    class Config:
        orm_mode = True


class DonationDB(DonationCreate, CharityBase):

    user_id: int

    class Config:
        orm_mode = True
