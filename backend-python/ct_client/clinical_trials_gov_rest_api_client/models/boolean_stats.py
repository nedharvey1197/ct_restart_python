from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.field_stats_type import FieldStatsType

T = TypeVar("T", bound="BooleanStats")


@_attrs_define
class BooleanStats:
    """
    Attributes:
        false_count (int):
        field (str):
        missing_studies_count (int):
        piece (str):
        true_count (int):
        type_ (FieldStatsType):
    """

    false_count: int
    field: str
    missing_studies_count: int
    piece: str
    true_count: int
    type_: FieldStatsType

    def to_dict(self) -> dict[str, Any]:
        false_count = self.false_count

        field = self.field

        missing_studies_count = self.missing_studies_count

        piece = self.piece

        true_count = self.true_count

        type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "falseCount": false_count,
                "field": field,
                "missingStudiesCount": missing_studies_count,
                "piece": piece,
                "trueCount": true_count,
                "type": type_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        false_count = d.pop("falseCount")

        field = d.pop("field")

        missing_studies_count = d.pop("missingStudiesCount")

        piece = d.pop("piece")

        true_count = d.pop("trueCount")

        type_ = FieldStatsType(d.pop("type"))

        boolean_stats = cls(
            false_count=false_count,
            field=field,
            missing_studies_count=missing_studies_count,
            piece=piece,
            true_count=true_count,
            type_=type_,
        )

        return boolean_stats
