from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field


class BaseOrganization(BaseModel):
    tax_code: Annotated[str, Field(...)]
    name: Annotated[str, Field(...)]
    address: Annotated[str, Field(...)]
    phone: Annotated[str | None, Field(default=None)]
    license_date: Annotated[datetime, Field(...)]
    rep_name: Annotated[str, Field(...)]
    source: Annotated[str, Field(...)]