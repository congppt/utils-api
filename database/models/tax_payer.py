from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from database.models import Entity


class TaxPayer(Entity):
    __tablename__ = "tax_payers"
    tax_code: Mapped[str] = mapped_column(primary_key=True)
    issue_date: Mapped[datetime]
    name: Mapped[str]
    address: Mapped[str]
    phone: Mapped[Optional[str]]
    id_number: Mapped[Optional[str]] = mapped_column(index=True, unique=True)
    license: Mapped[Optional[str]]
    license_issuer: Mapped[Optional[str]]
    rep_name: Mapped[Optional[str]]
    rep_address: Mapped[Optional[str]]
    source: Mapped[str]
