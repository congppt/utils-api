from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from database import aget_db
from features.tax import handler
from features.tax.exception import OrganizationNotFoundException

router = APIRouter(prefix="/tax")

@router.get("/{tax_code}")
async def find_org_by_tax_code(tax_code: Annotated[str, Path(min_length=10, max_length=14)], db: AsyncSession = Depends(aget_db)):
    try:
        return await handler.find_tax_code(tax_code=tax_code, db=db)
    except OrganizationNotFoundException:
        raise HTTPException(status_code=404)
