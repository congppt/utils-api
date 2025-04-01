from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cache import aget_cache, aset_cache
from database.models.tax_payer import TaxPayer
from external.tax.mst import MSTTaxService
from features.tax.exception import TaxPayerNotFoundError
from features.tax.schema import TaxPayerResponse

async def find_tax_payer(tax_identifier: str, db: AsyncSession) -> TaxPayerResponse | None:
    # tìm trong cache
    key = f"tax_{tax_identifier}"
    if payer:=await aget_cache(key, TaxPayerResponse):
        return payer # type: ignore
    # tìm trong db
    if payer_ent:=await db.scalar(select(TaxPayer).filter(TaxPayer.tax_code == tax_identifier)):
        payer = TaxPayerResponse.model_validate(payer_ent)
        await aset_cache(key, payer, 60 * 60)
        return payer
    # tìm trên các site bên ngoài
    external_services= (MSTTaxService,)
    for service in external_services:
        ext_payer = await service.get_tax_payer(tax_identifier=tax_identifier)
        if not ext_payer:
            continue
        payer = TaxPayerResponse.model_validate(ext_payer)
        # set cache & lưu db
        await aset_cache(key, payer, 60 * 60)
        db.add(TaxPayer(**payer.model_dump()))
        await db.commit()
        return payer
    raise TaxPayerNotFoundError()