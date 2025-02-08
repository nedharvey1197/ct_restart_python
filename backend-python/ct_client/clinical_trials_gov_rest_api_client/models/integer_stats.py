from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..models.field_stats_type import FieldStatsType
from ..types import UNSET, Unset

T = TypeVar("T", bound="IntegerStats")


@_attrs_define
class IntegerStats:
    """
    Attributes:
        field (str):
        missing_studies_count (int):
        piece (str):
        type_ (FieldStatsType):
        avg (Union[Unset, float]):
        max_ (Union[Unset, int]):
        min_ (Union[Unset, int]):
    """

    field: str
    missing_studies_count: int
    piece: str
    type_: FieldStatsType
    avg: Union[Unset, float] = UNSET
    max_: Union[Unset, int] = UNSET
    min_: Union[Unset, int] = UNSET

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        missing_studies_count = self.missing_studies_count

        piece = self.piece

        type_ = self.type_.value

        avg = self.avg

        max_ = self.max_

        min_ = self.min_

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "field": field,
                "missingStudiesCount": missing_studies_count,
                "piece": piece,
                "type": type_,
            }
        )
        if avg is not UNSET:
            field_dict["avg"] = avg
        if max_ is not UNSET:
            field_dict["max"] = max_
        if min_ is not UNSET:
            field_dict["min"] = min_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        field = d.pop("field")

        missing_studies_count = d.pop("missingStudiesCount")

        piece = d.pop("piece")

        type_ = FieldStatsType(d.pop("type"))

        avg = d.pop("avg", UNSET)

        max_ = d.pop("max", UNSET)

        min_ = d.pop("min", UNSET)

        integer_stats = cls(
            field=field,
            missing_studies_count=missing_studies_count,
            piece=piece,
            type_=type_,
            avg=avg,
            max_=max_,
            min_=min_,
        )

        return integer_stats
