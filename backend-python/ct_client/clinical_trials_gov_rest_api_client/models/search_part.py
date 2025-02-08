from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

T = TypeVar("T", bound="SearchPart")


@_attrs_define
class SearchPart:
    """
    Attributes:
        is_enum (bool):
        is_synonyms (bool):
        pieces (list[str]):
        type_ (str):
        weight (float):
    """

    is_enum: bool
    is_synonyms: bool
    pieces: list[str]
    type_: str
    weight: float

    def to_dict(self) -> dict[str, Any]:
        is_enum = self.is_enum

        is_synonyms = self.is_synonyms

        pieces = self.pieces

        type_ = self.type_

        weight = self.weight

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "isEnum": is_enum,
                "isSynonyms": is_synonyms,
                "pieces": pieces,
                "type": type_,
                "weight": weight,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        is_enum = d.pop("isEnum")

        is_synonyms = d.pop("isSynonyms")

        pieces = cast(list[str], d.pop("pieces"))

        type_ = d.pop("type")

        weight = d.pop("weight")

        search_part = cls(
            is_enum=is_enum,
            is_synonyms=is_synonyms,
            pieces=pieces,
            type_=type_,
            weight=weight,
        )

        return search_part
