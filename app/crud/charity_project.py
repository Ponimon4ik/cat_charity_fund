from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, false

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    @staticmethod
    async def get_project_by_name(
            project_name: str,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == project_name
            )
        )
        project = project.scalars().first()
        return project

    async def get_not_fully_invested_objects(
            self,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        objects = await session.execute(
            select(CharityProject).order_by(
                CharityProject.create_date
            ).where(
                CharityProject.fully_invested == false()
            )
        )
        objects = objects.scalars().all()
        return objects


charity_project_crud = CRUDCharityProject(CharityProject)
