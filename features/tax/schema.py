from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field


class OrganizationResponse(BaseModel):
    tax_code: Annotated[str, Field(...)]
    name: Annotated[str, Field(...)]
    address: Annotated[str, Field(...)]
    phone: Annotated[str | None, Field(default=None)]
    license: Annotated[str | None, Field(default=None)]
    license_date: Annotated[datetime, Field(...)]
    license_issuer: Annotated[str | None, Field(default=None)]
    rep_name: Annotated[str, Field(...)]
    rep_address: Annotated[str | None, Field(default=None)]
    source: Annotated[str, Field(...)]

    model_config=ConfigDict(from_attributes=True)