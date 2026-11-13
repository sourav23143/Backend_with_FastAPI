
# SERVICE FOR DATABASE INTERACTION FOR SELLER  
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.seller import SellerCreate
from app.database.models import Seller
from passlib.context import CryptContext

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