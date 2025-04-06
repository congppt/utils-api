from __future__ import annotations
from typing import Annotated

from pydantic import BaseModel, Field


class Area(BaseModel):
    id: Annotated[int, Field(...)]
    name: Annotated[str, Field(...)]
    areas: Annotated[list[Area], Field()] = []
    
