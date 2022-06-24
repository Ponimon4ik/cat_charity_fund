from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.base import CharityBase


class CharityProject(Base, CharityBase):

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

