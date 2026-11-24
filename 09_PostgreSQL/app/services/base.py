from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel


class BaseService:
    def __init__(self, model: SQLModel, session: AsyncSession):
        # Get database session to perform database operations
        self.model = model
        self.session = session 

    async def _get(self, id: UUID): # "_" since so that we can access this method where it is being inherited, but not in the endpoint where service is used as dependency
        return await self.session.get(self.model, id)

    async def _add(self, entity: SQLModel ):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)

        return entity 

    async def _update(self, entity: SQLModel):
        return await self._create(entity)
        # when updating data, adding it to the session is not required, but we will do that to be on the safer side

    async def _delete(self, entity: SQLModel):
        await self.session.delete(entity)