from datetime import datetime as dt
from typing import Union, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crude
from app.models import Donation, CharityProject


async def investing(
    source: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:
    database_objects = (
        await donation_crude.get_not_fully_invested(session)
        if source.__class__ is CharityProject
        else await charity_project_crud.get_not_fully_invested(session)
    )
    source.invested_amount = 0
    for target in database_objects:
        remains_of_source = (
            source.full_amount - source.invested_amount
        )
        remains_of_target = (
            target.full_amount - target.invested_amount
        )
        if remains_of_source > remains_of_target:
            target.invested_amount += remains_of_target
            source.invested_amount += remains_of_target
        else:
            target.invested_amount += remains_of_source
            source.invested_amount += remains_of_source
        if target.full_amount == target.invested_amount:
            target.fully_invested = True
            target.close_date = dt.now()
        session.add(target)
        if source.full_amount == source.invested_amount:
            source.fully_invested = True
            source.close_date = dt.now()
            break
    return source
