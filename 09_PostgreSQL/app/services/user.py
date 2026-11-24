from fastapi import HTTPException, status
from passlib.context import CryptContext
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User, Seller
from app.utils import generate_access_token

from .base import BaseService


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService(BaseService):
    def __init__(self, model: User, session: AsyncSession):
        self.model = model
        self.session = session 


    # Get User by email
    async def _get_by_email(self, email) -> User | None:
        return await self.session.scalar(
            select(self.model).where(self.model.email == email)
        )
        # after executing this statement, we will get back result. and from the result, we can get the scalar value(i.e our user class)

    async def _add_user(self, data: dict):
        # User instantation
        user = self.model(
             **data,
             password_hash=password_context.hash(data["password"])
        )

        # adding user to database
        return await self._add(user) 

    async def token(self, email, password) -> str:
            # Validate the credentials
            user = await self._get_by_email(email)
    
            if user is None or not password_context.verify(
                        password, # plain password (secret)
                        user.password_hash, #password hash
                    ):
                raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail = "Email or password is incorrect",
                )
    

            # JWT token generation 
            return  generate_access_token(data={
                "user": {
                    "name": user.name,
                    "id": str(user.id),   # because seller.id is in UUID type, it cannot be encoded in json format , so we have changed it to string type, so beacuse here we enoded then we have use uuid, then have smae to do when decoded
                }
            })
    
            