from datetime import datetime as dt
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, CharityProject


async def investing(
    source: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    source.invested_amount = 0
    for target in await CRUDBase(
            Donation if source.__class__ is CharityProject else CharityProject
    ).get_not_fully_invested(session):
        allocated_amount = (
            (target.full_amount - target.invested_amount) if
            (source.full_amount - source.invested_amount) >
            (target.full_amount - target.invested_amount) else
            (source.full_amount - source.invested_amount)
        )
        target.invested_amount += allocated_amount
        source.invested_amount += allocated_amount
        session.add(target)
        for object in (target, source):
            if object.full_amount == object.invested_amount:
                object.fully_invested, object.close_date = True, dt.now()
                if object is source:
                    break
    return source
