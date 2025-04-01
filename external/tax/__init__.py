from abc import ABC, abstractmethod

from external.tax.schema import ExternalTaxPayer


class TaxService(ABC):
    @classmethod
    @abstractmethod
    async def get_tax_payer(cls, tax_code: str) -> ExternalTaxPayer | None:
        return None
