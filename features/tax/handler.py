from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cache import aget_cache, aset_cache
from database.models.organization import Organization
from external.tax.mst import MSTTaxService
from features.tax.exception import OrganizationNotFoundException
from features.tax.schema import OrganizationResponse

async def find_tax_code(tax_code: str, db: AsyncSession) -> OrganizationResponse | None:
    # tìm trong cache
    key = f"tax_code_{tax_code}"
    if org:=await aget_cache(key, OrganizationResponse):
        return org # type: ignore
    # tìm trong db
    if org_ent:=await db.scalar(select(Organization).filter(Organization.tax_code == tax_code)):
        org = OrganizationResponse.model_validate(org_ent)
        await aset_cache(key, org, 60 * 60)
        return org
    # tìm trên các site bên ngoài
    external_services= (MSTTaxService,)
    for service in external_services:
        ext_org = await service.find_organization(tax_code=tax_code)
        if not ext_org:
            continue
        org = OrganizationResponse.model_validate(ext_org)
        # set cache & lưu db
        await aset_cache(key, org, 60 * 60)
        db.add(Organization(**org.model_dump()))
        await db.commit()
        return org
    raise OrganizationNotFoundException()