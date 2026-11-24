
# SERVICE FOR DATABASE INTERACTION FOR SELLER  
from datetime import datetime, timedelta

from fastapi import HTTPException, status
import jwt
from sqlalchemy.ext.asyncio import AsyncSession


from app.utils import generate_access_token
from app.config import security_settings
from app.api.schemas.seller import SellerCreate
from app.database.models import Seller
from passlib.context import CryptContext
from sqlalchemy import select

from .user import UserService

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





class SellerService(UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(Seller, session)

    async def add(self, seller_create: SellerCreate) -> Seller:
        # creating a new seller
        return await self._add_user(seller_create.model_dump())


    async def token(self, email, password) -> str:
        
        return await self._generate_token(email, password)











# class SellerService():
#     def __init__(self, session: AsyncSession):
#         # Get database session to perform database operations
#         self.session = session 

#     async def add(self, credentials: SellerCreate) -> Seller:
#         # creating a new seller
#         seller = Seller(
#             **credentials.model_dump(exclude={"password"}),
#             #beacuse in our Seller model we will have "password_hash" filed and, in SellerCreate, we will have "password" filed and because these doesnot match it will not be included inside **credentials.model_dump()
#             #hashed password
#             password_hash=password_context.hash(credentials.password),
#         )
#         # we will go ahead and fill name and email simply and that for password, we have to hash and then add it to our database 

#         # now we get the hash version of our password, which we store inside our database(i.e SQLModel)
#         #now our seller model is ready to be added to in our database

#         self.session.add(seller)
#         await self.session.commit()
#         await self.session.refresh(seller)

#         return seller

#     async def token(self, email, password) -> str:
#         # Validate the credentials

#         # Checking if we have any record in database with given email
#         # self.session.get(Seller, email) # generally it will work, but in this case it won't, because email is not primary key, insted id is primary key, so when we get get method on seesion we have to provide that as well 
#         result = await self.session.execute(
#             select(Seller).where(Seller.email == email)
#         ) # custom sql query with sqlachemy 

#         seller = result.scalar() #Fetch the first column of the first row, and close the result set.


#         # self.session.get(Seller, seller.id) >> we will add this data in access token insted so it will be easier for us to find the data and later on 

#         if seller is None or not password_context.verify(
#                     password, # plain password (secret)
#                     seller.password_hash, #password hash
#                 ):
#             raise HTTPException(
#                 status_code= status.HTTP_404_NOT_FOUND,
#                 detail = "Email or password is incorrect",
#             )

#         # # JWT Token generation
#         # token = jwt.encode(
#         #     payload={
#         #     "user": {
#         #         "name": seller.name,
#         #         "email": seller.email
#         #     },#beacuse we have already validated seller, we don't need password in the payload, Optionally, if we wnat we can use another filed which can be used to expire this jwt token
#         #     "exp" : datetime.now() + timedelta(days=1),
#         #     },
#         #     algorithm=security_settings.JWT_ALGORITHM,
#         #     key= security_settings.JWT_SECRET, # insted of hardcoding them in this JWT encode function, we can pull them out as environment variable, so we can share them later on 
#         # )


#         # return token 

    
#         # so once we have validated a seller, now we can go ahead and encode the seller data into a token and provide it back as well 
#         #FOR THIS WE HAVE TO GENERATE JWT TOKEN AND FOR CREATING JWT TOKEN WE NEED SPECIAL LIBRARY (IN PYTHON WE USE pyjwt)
#         # when we install it called "pyjwt" and when we use it it called only "jwt" 

#         # JWT token generation 
#         token = generate_access_token(data={
#             "user": {
#                 "name": seller.name,
#                 "id": str(seller.id),   # because seller.id is in UUID type, it cannot be encoded in json format , so we have changed it to string type, so beacuse here we enoded then we have use uuid, then have smae to do when decoded
#             }
#         })

#         return token