from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class ExternalTaxPayer(BaseModel):
    tax_code: Annotated[str, Field(...)]
    issue_date: Annotated[datetime, Field(...)]
    name: Annotated[str, Field(...)]
    address: Annotated[str, Field(...)]
    phone: Annotated[str | None, Field()] = None
    id_number: Annotated[str | None, Field()] = None
    rep_name: Annotated[str | None, Field()] = None
    source: Annotated[str, Field(...)]
