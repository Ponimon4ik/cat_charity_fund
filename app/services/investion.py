from datetime import datetime as dt
from typing import Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crude
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models.user import User
from app.schemas.charity_project import CharityProjectCreate
from app.schemas.donation import DonationCreate

PROJECT_OR_DONATION = {
    True: [CharityProject, donation_crude],
    False: [Donation, charity_project_crud]
}


async def investing(
    object_for_database: Union[DonationCreate, CharityProjectCreate],
    session: AsyncSession,
    user: Optional[User] = None,
    project: bool = False
) -> Union[Donation, CharityProject]:
    object_data_for_database = object_for_database.dict()
    model, crud = PROJECT_OR_DONATION[project]
    database_objects = await crud.get_not_fully_invested(session)
    if model == Donation:
        object_data_for_database['user_id'] = user.id
    if not database_objects:
        if model == Donation:
            object = await donation_crude.create(object_data_for_database, session)
            return object
        object = await charity_project_crud.create(object_data_for_database, session)
        return object
    object_data_for_database['invested_amount'] = 0
    for base_object in database_objects:
        free_amount_of_object_data = object_for_database.full_amount - object_data_for_database['invested_amount']
        free_amount_of_base_object = base_object.full_amount - base_object.invested_amount
        if free_amount_of_object_data > free_amount_of_base_object:
            base_object.invested_amount += free_amount_of_base_object
            object_data_for_database['invested_amount'] += free_amount_of_base_object
        else:
            base_object.invested_amount += free_amount_of_object_data
            object_data_for_database['invested_amount'] += free_amount_of_object_data
        if base_object.full_amount == base_object.invested_amount:
            base_object.fully_invested = True
            base_object.close_date = dt.now()
        session.add(base_object)
        if object_data_for_database['invested_amount'] == object_for_database.full_amount:
            object_data_for_database.update([
                ('fully_invested', True),
                ('close_date', dt.now())
            ])
            break
    object = model(**object_data_for_database)
    session.add(object)
    await session.commit()
    await session.refresh(object)
    return object
