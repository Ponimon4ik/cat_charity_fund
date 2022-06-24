from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project = await charity_project_crud.get_project_by_name(project_name, session)
    if project:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_project(
        project_id: int,
        session: AsyncSession
) -> Optional[CharityProject]:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=404,
            detail='Проект не найден'
        )
    return project


async def check_full_amount(

):
    pass

