from datetime import datetime as dt

from sqlalchemy import DATETIME, Boolean, Column, Integer


class CharityBase:

    full_amount = Column(Integer, nullable=False, )
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DATETIME, default=dt.now)
    close_date = Column(DATETIME)
