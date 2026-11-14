
# SERVICE FOR DATABASE INTERACTION FOR SELLER  
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.seller import SellerCreate
from app.database.models import Seller
from passlib.context import CryptContext
from sqlalchemy import select

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SellerService:
    def __init__(self, session: AsyncSession):
        # Get database session to perform database operations
        self.session = session 

    async def add(self, credentials: SellerCreate) -> Seller:
        # creating a new seller
        seller = Seller(
            **credentials.model_dump(exclude={"password"}),
            #beacuse in our Seller model we will have "password_hash" filed and, in SellerCreate, we will have "password" filed and because these doesnot match it will not be included inside **credentials.model_dump()
            #hashed password
            password_hash=password_context.hash(credentials.password),
        )
        # we will go ahead and fill name and email simply and that for password, we have to hash and then add it to our database 

        # now we get the hash version of our password, which we store inside our database(i.e SQLModel)
        #now our seller model is ready to be added to in our database

        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)

        return seller

    async def token(self, email, password) -> str:
        # Validate the credentials

        # Checking if we have any record in database with given email
        # self.session.get(Seller, email) # generally it will work, but in this case it won't, because email is not primary key, insted id is primary key, so when we get get method on seesion we have to provide that as well 
        result = await self.session.execute(
            select(Seller).where(Seller.email == email)
         ) # custom sql query with sqlachemy 

        seller = result.scalar() #Fetch the first column of the first row, and close the result set.

        if seller is None or password_context.verify(
                    password, # plain password (secret)
                    seller.password_hash, #password hash
                ):
            raise HTTPException(
                status_code= status.HTTP_404_NOT_FOUND,
                detail = "Email or password is incorrect",
            )

        seller # verified

        
        # so once we have validated a seller, now we can go ahead and encode the seller data into a token and provide it back as well 