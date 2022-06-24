from datetime import datetime as dt

from typing import Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crude
from app.models.user import User
from app.schemas.donation import DonationCreate
from app.schemas.charity_project import CharityProjectCreate


async def investion(
    object_for_database: Union[DonationCreate, CharityProjectCreate],
    session: AsyncSession,
    user: Optional[User] = None,
    project: bool = False
) -> Union[Donation, CharityProject]:
    object_data_for_database = object_for_database.dict()
    if project:
        database_objects = await donation_crude.get_not_fully_invested(session)
        if not database_objects:
            object = await charity_project_crud.create(object_for_database, session)
            return object
        model = CharityProject
    else:
        database_objects = await charity_project_crud.get_not_fully_invested(session)
        if not database_objects:
            object = await donation_crude.create(object_for_database, session)
            return object
        model = Donation
        object_data_for_database['user_id'] = user.id
    object_data_for_database['invested_amount'] = 0
    for base_object in database_objects:
        free_amount_of_object_data = object_for_database.full_amount - object_data_for_database['invested_amount']
        free_amount_of_base_object = base_object.full_amount - base_object.invested_amount
        if free_amount_of_object_data > free_amount_of_base_object:
            base_object.invested_amount += free_amount_of_base_object
            base_object.fully_invested = True
            base_object.close_date = dt.now()
            object_data_for_database['invested_amount'] += free_amount_of_base_object
            session.add(base_object)
            continue
        base_object.invested_amount += free_amount_of_object_data
        object_data_for_database['invested_amount'] += free_amount_of_object_data
        object_data_for_database.update([
            ('fully_invested', True),
            ('close_date', dt.now())
        ])
        if base_object.full_amount == base_object.invested_amount:
            base_object.fully_invested = True
            base_object.close_date = dt.now()
        session.add(base_object)
        break
    object = model(**object_data_for_database)
    session.add(object)
    await session.commit()
    await session.refresh(object)
    return object

# async def investion(
#     object_for_database: Union[DonationCreate, CharityProjectCreate],
#     session: AsyncSession,
#     user: Optional[User] = None,
#     project: bool = False
# ) -> Union[Donation, CharityProject]:
#     object_data_for_database = object_for_database.dict()
#     if project:
#         database_objects = await donation_crude.get_not_fully_invested(session)
#         if not database_objects:
#             object = await charity_project_crud.create(object_for_database, session)
#             return object
#         model = CharityProject
#     else:
#         database_objects = await charity_project_crud.get_not_fully_invested(session)
#         if not database_objects:
#             object = await donation_crude.create(object_for_database, session)
#             return object
#         model = Donation
#         object_data_for_database['user_id'] = user.id
#     object_data_for_database['invested_amount'] = 0
#     for base_object in database_objects:
#         free_amount_of_object_data = object_for_database.full_amount - object_data_for_database['invested_amount']
#         free_amount_of_base_object = base_object.full_amount - base_object.invested_amount
#         if free_amount_of_object_data > free_amount_of_base_object:
#             base_object.invested_amount += free_amount_of_base_object
#             # base_object.fully_invested = True
#             # base_object.close_date = dt.now()
#             object_data_for_database['invested_amount'] += free_amount_of_base_object
#             # session.add(base_object)
#             # continue
#         else:
#             base_object.invested_amount += free_amount_of_object_data
#             object_data_for_database['invested_amount'] += free_amount_of_object_data
#             object_data_for_database.update([
#                 ('fully_invested', True),
#                 ('close_date', dt.now())
#             ])
#             if base_object.full_amount == base_object.invested_amount:
#                 base_object.fully_invested = True
#                 base_object.close_date = dt.now()
#             session.add(base_object)
#             break
#     object = model(**object_data_for_database)
#     session.add(object)
#     await session.commit()
#     await session.refresh(object)
#     return object
