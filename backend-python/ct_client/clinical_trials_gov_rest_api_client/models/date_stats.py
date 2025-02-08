from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..models.field_stats_type import FieldStatsType
from ..types import UNSET, Unset

T = TypeVar("T", bound="DateStats")


@_attrs_define
class DateStats:
    """
    Attributes:
        field (str):
        formats (list[str]):
        missing_studies_count (int):
        piece (str):
        type_ (FieldStatsType):
        max_ (Union[Unset, str]):
        min_ (Union[Unset, str]):
    """

    field: str
    formats: list[str]
    missing_studies_count: int
    piece: str
    type_: FieldStatsType
    max_: Union[Unset, str] = UNSET
    min_: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        formats = self.formats

        missing_studies_count = self.missing_studies_count

        piece = self.piece

        type_ = self.type_.value

        max_ = self.max_

        min_ = self.min_

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "field": field,
                "formats": formats,
                "missingStudiesCount": missing_studies_count,
                "piece": piece,
                "type": type_,
            }
        )
        if max_ is not UNSET:
            field_dict["max"] = max_
        if min_ is not UNSET:
            field_dict["min"] = min_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        field = d.pop("field")

        formats = cast(list[str], d.pop("formats"))

        missing_studies_count = d.pop("missingStudiesCount")

        piece = d.pop("piece")

        type_ = FieldStatsType(d.pop("type"))

        max_ = d.pop("max", UNSET)

        min_ = d.pop("min", UNSET)

        date_stats = cls(
            field=field,
            formats=formats,
            missing_studies_count=missing_studies_count,
            piece=piece,
            type_=type_,
            max_=max_,
            min_=min_,
        )

        return date_stats
