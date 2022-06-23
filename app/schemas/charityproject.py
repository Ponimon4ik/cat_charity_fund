from pydantic import BaseModel, PositiveInt, Field

from app.schemas.base import CharityBase


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectCreate):
    pass


class CharityProjectDB(CharityBase, CharityProjectUpdate):

    class Config:
        orm_mode = True
