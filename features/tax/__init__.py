from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import aget_db

router = APIRouter(prefix="tax")

@router.get("/{tax_code}")
async def find_org_by_tax_code(tax_code: str, db: AsyncSession = Depends(aget_db)):
    pass