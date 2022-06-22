from sqlalchemy import Column, Integer, ForeignKey, Text

from app.core.db import Base
from app.models.base import CharityBase


class Donation(Base, CharityBase):

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
