from abc import ABC, abstractmethod

from external.tax.schema import BaseOrganization


class TaxService(ABC):
    @classmethod
    @abstractmethod
    async def find_organization(cls, tax_code: str) -> BaseOrganization | None:
        pass
