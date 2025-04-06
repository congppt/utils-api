from typing import Annotated
from fastapi import APIRouter, Query

from features.area import handler


router = APIRouter(prefix="/area")


@router.get("/vi")
async def get_vietnam_areas(ids: Annotated[list[int], Query()] = [], minimal: bool = True):
    return handler.get_areas(ids=ids, minimal=minimal)
