from datetime import datetime as dt
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, CharityProject


async def investing(
    source: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    if not source.invested_amount:
        source.invested_amount = 0
    crud = CRUDBase(Donation) if isinstance(
        source, CharityProject) else CRUDBase(CharityProject)
    for target in await crud.get_not_fully_invested(session):
        session.add(target)
        allocated_amount = (
            (target.full_amount - target.invested_amount)
            if (source.full_amount - source.invested_amount) >
               (target.full_amount - target.invested_amount) else
            (source.full_amount - source.invested_amount)
        )
        for object in (target, source):
            object.invested_amount += allocated_amount
            if object.invested_amount == object.full_amount:
                object.fully_invested, object.close_date = True, dt.now()
        if source.fully_invested:
            break
    return source
