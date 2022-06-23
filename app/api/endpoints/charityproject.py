from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models.charityproject import CharityProject
from app.core.user import current_superuser
from app.schemas.charityproject import CharityProjectDB, CharityProjectUpdate ,CharityProjectCreate
from app.crud.charityproject import charity_project_crud
from app.api.validators import check_name_duplicate, check_project

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
) -> List[CharityProject]:
    """Только для суперюзеров."""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],

)
async def create_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """Только для суперюзеров."""
    project = await check_project(project_id, session)
    if obj_in.name:
        if obj_in.name != project.name:
            await check_name_duplicate(obj_in.name, session)
    project = await charity_project_crud.update(project, obj_in, session)
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """Только для суперюзеров."""
    project = await check_project(project_id, session)
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=422,
            detail='Нельзя удалить проект, '
                   'в который уже были инвестированы средства, '
                   'его можно только закрыть.'
        )
    project = await charity_project_crud.remove(
        project, session
    )
    return project
