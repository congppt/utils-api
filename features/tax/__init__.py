from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from database import aget_db
from features.tax import handler
from features.tax.exception import TaxPayerNotFoundError

router = APIRouter(prefix="/tax")


@router.get("/{tax_identifier}")
async def find_tax_payer(
    tax_identifier: Annotated[str, Path(min_length=10, max_length=14)],
    db: AsyncSession = Depends(aget_db),
):
    try:
        return await handler.find_tax_payer(tax_identifier=tax_identifier, db=db)
    except TaxPayerNotFoundError:
        raise HTTPException(status_code=404)
