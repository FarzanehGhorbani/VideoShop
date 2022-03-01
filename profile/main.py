from fastapi import APIRouter

from .dependencies import token_required,JWTBearer
from fastapi import Request
from .models import Country
router = APIRouter(
    prefix="/profile",
    tags=['Profile']
)



@router.post("/edit")
@JWTBearer
async def root(request:Request):
    print('--------------------------------')
    return {"message": "Hello World"}












