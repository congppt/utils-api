from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


class Organization(Base):
    __tablename__ = "organizations"
    tax_code: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    address: Mapped[str]
    phone: Mapped[Optional[str]]
    license: Mapped[str]
    license_date: Mapped[datetime]
    license_issuer: Mapped[str]
    rep_name: Mapped[str]
    rep_address: Mapped[str]