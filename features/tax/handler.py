from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from cache import aget_cache, aset_cache
from database.models.organization import Organization

async def find_tax_code(tax_code: str, db: AsyncSession):
    # tìm trong cache
    key = f"tax_code_{tax_code}"
    org = await aget_cache(key)
    if org:
        pass
    # tìm trong db
    query = select(Organization).filter(Organization.tax_code == tax_code)
    result = await db.execute(query)
    if org:=result.scalar_one_or_none():
        pass
    # tìm trên tracuunnt.gdt.gov.vn

    # tìm trên masothue.com
    
    if not org:
        return None
    # set cache & lưu db
    await aset_cache(key, org, 60 * 60)
    db.add(org)
    await db.commit()
    return org