from dataclasses import dataclass
from typing import Generic

from super_cereal.cerealizer import Cerealizer, V, T


@dataclass
class Encrypted(Generic[T]):
    key_id: str
    value: T


class ExceptionCerealizer(Cerealizer[Encrypted[T]]):
    def supported_types(self) -> T:
        return Encrypted

    def serialize(self, obj: Encrypted[T]) -> V:
        pass

    def deserialize(self, obj: V, t: T) -> T:
        pass
