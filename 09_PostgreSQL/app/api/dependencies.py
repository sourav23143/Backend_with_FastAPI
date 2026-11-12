
# IT WILL CONTAINS DEPENDENCIES OF OUR ENDPOINTS
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.database.session import get_session
from app.services.shipment import ShipmentService

SessionDep = Annotated[AsyncSession, Depends(get_session)]  # When we hint on arguments type like this Annotation fastapi will check metadata and when it sees it is a Depends ,that is a dependency, it goes ahead and runs the function provided inside it


def get_shipment_service(session: SessionDep):
    return ShipmentService(session)
#and because we not use any await keyword or handle any coroutines during initialization, we can make this normal function as well, because when it is not required we can skip asynchronous part 

ServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]