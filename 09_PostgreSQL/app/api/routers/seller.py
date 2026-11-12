from fastapi import APIRouter

from ..schemas.seller import SellerCreate




router = APIRouter(prefix="/seller")

# endpoint to create a new seller
@router.post("/signup")
def register_seller(seller: SellerCreate):
    pass 
