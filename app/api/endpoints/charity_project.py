from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.models.charity_project import CharityProject
from app.core.user import current_superuser
from app.schemas.charity_project import CharityProjectDB, CharityProjectUpdate, CharityProjectCreate
from app.crud.charity_project import charity_project_crud
from app.api.validators import check_name_duplicate, check_project
from app.services.investion import investion

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    # dependencies=[Depends(current_superuser)]
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session)
) -> List[CharityProject]:
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],


)
async def create_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
) -> CharityProject:
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await investion(
        object_for_database=project,
        session=session,
        project=True
    )
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
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
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
            status_code=400,
            detail='В проект были внесены средства, '
                   'не подлежит удалению!'
        )
    project = await charity_project_crud.remove(
        project, session
    )
    return project
