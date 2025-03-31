from external.tax import TaxService
from external.tax.mst.schema import MSTOrganization


class MSTTaxService(TaxService):
    BASE_URL = "https://masothue.com"
    @classmethod
    async def find_organization(cls, tax_code: str) -> MSTOrganization | None:
        pass