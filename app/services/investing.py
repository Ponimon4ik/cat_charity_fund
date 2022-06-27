from datetime import datetime as dt
from typing import Union, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crude
from app.schemas.charity_project import CharityProjectCreate
from app.schemas.donation import DonationCreate


OBJECTS_NOT_FULLY_INVESTED = {
    CharityProjectCreate: donation_crude.get_not_fully_invested,
    DonationCreate: charity_project_crud.get_not_fully_invested
}


async def investing(
    object_for_database: Union[DonationCreate, CharityProjectCreate],
    session: AsyncSession,
) -> Dict:
    object_data_for_database = object_for_database.dict()
    database_objects = await OBJECTS_NOT_FULLY_INVESTED[
        type(object_for_database)
    ](session)
    object_data_for_database['invested_amount'] = 0
    for base_object in database_objects:
        free_amount_of_object_data = (
            object_for_database.full_amount -
            object_data_for_database['invested_amount']
        )
        free_amount_of_base_object = (
            base_object.full_amount - base_object.invested_amount
        )
        if free_amount_of_object_data > free_amount_of_base_object:
            base_object.invested_amount += free_amount_of_base_object
            object_data_for_database['invested_amount'] += (
                free_amount_of_base_object
            )
        else:
            base_object.invested_amount += free_amount_of_object_data
            object_data_for_database['invested_amount'] += (
                free_amount_of_object_data
            )
        if base_object.full_amount == base_object.invested_amount:
            base_object.fully_invested = True
            base_object.close_date = dt.now()
        session.add(base_object)
        if (
                object_data_for_database['invested_amount'] ==
                object_for_database.full_amount
        ):
            object_data_for_database.update([
                ('fully_invested', True),
                ('close_date', dt.now())
            ])
            break
    return object_data_for_database
