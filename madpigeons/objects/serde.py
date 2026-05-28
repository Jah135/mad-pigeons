from typing import Any, TYPE_CHECKING
import json

from . import wood, stone, glass, special, bird, pig
from .entity import Entity

if TYPE_CHECKING:
    from .level import Level


class EntitySnapshot:
    data: dict[str, Any]
    creator: type[Entity]

    def __init__(self, entity: Entity) -> None:
        self.data = dict()
        self.creator = entity.__class__

        entity.write_snapshot(self.data)

    def recreate(self, level: Level) -> Entity:
        return self.creator.from_snapshot(level, self.data)

    @property
    def serializable(self) -> dict[str, Any]:
        return {
            "t": f"{self.creator.__module__}.{self.creator.__name__}",
            "d": self.data,
        }


DECODE_SERIALIZE_MAP: dict[str, type[Entity]] = dict()

for module in [wood, stone, glass, special, bird, pig]:
    module_name = module.__name__

    for class_name, class_type in module.__dict__.items():
        if not isinstance(class_type, type(Entity)):
            continue

        DECODE_SERIALIZE_MAP[f"{module_name}.{class_name}"] = class_type


# def load_entity_from_json(entity_json: str, level: Level) -> Entity | None:
#     json_object: dict = loads(entity_json)

#     class_name: str | None = json_object.get("t", None)

#     if class_name is None:
#         return

#     class_type = DECODE_SERIALIZE_MAP.get(class_name)

#     if class_type is None:
#         return

#     entity_data: dict = json_object.get("d", {})

#     return class_type.from_snapshot(level, entity_data)


def load_entities_from_file(path: str, level: Level) -> list[Entity]:
    loaded_entities = []

    with open(path, "r") as f:
        entities_data: list[dict] = json.load(f)

        for entity_info in entities_data:
            class_name = entity_info.get("t")

            if class_name is None:
                continue

            class_type = DECODE_SERIALIZE_MAP.get(class_name)

            if class_type is None:
                continue

            loaded_entities.append(
                class_type.from_snapshot(level, entity_info.get("d", []))
            )

    return loaded_entities


def save_snapshots_to_file(snapshots: list[EntitySnapshot], path: str):
    with open(path, "w") as f:
        f.write(json.dumps([a.serializable for a in snapshots]))
