from typing import Optional

from pydantic import (
    BaseModel, Extra, Field, PositiveInt, root_validator
)

from app.schemas.base import CharityBase


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):

    @root_validator()
    def values_is_not_null(cls, values):
        for value in values:
            if values[value] == '':
                raise ValueError(f'Нельзя назначать пустое {value}')
        return values


class CharityProjectCreate(CharityProjectUpdate):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectDB(CharityBase, CharityProjectCreate):

    class Config:
        orm_mode = True
