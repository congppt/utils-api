import json
import os

from features.area.exception import AreaNotFoundError
from features.area.schema import Area


def __initialize():
    with open(os.path.dirname(os.path.abspath(__file__)) +"/data.json", "r") as f:
        data = json.load(f)

    def to_areas(areas: list[dict]) -> list[Area]:
        return [
            Area(id=index, name=area["name"], areas=to_areas(area.get("areas", [])))
            for index, area in enumerate(areas)
        ]

    return to_areas(data)


__AREAS = __initialize()


def get_areas(ids: list[int], minimal: bool):
    area: Area | None = None
    for id in ids:
        try:
            area = area.areas[id] if area else __AREAS[id]
        except IndexError:
            raise AreaNotFoundError()
    areas = area.areas if area else __AREAS
    return [Area(id=area.id, name=area.name) for area in areas] if minimal else areas