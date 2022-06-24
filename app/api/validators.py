from typing import Optional
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


NAME_DUPLICATE = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден'
FORBID_UPDATE_PROJECT = 'Закрытый проект нельзя редактировать!'


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project = await charity_project_crud.get_project_by_name(project_name, session)
    if project:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=NAME_DUPLICATE
        )


async def check_project(
        project_id: int,
        session: AsyncSession
) -> Optional[CharityProject]:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=PROJECT_NOT_FOUND
        )
    return project


def check_fully_invested_project(
        project: CharityProject
) -> None:
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=FORBID_UPDATE_PROJECT
        )
