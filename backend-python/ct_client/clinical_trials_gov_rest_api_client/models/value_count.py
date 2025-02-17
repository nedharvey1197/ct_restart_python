from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ValueCount")


@_attrs_define
class ValueCount:
    """
    Attributes:
        studies_count (int):
        value (str):
    """

    studies_count: int
    value: str

    def to_dict(self) -> dict[str, Any]:
        studies_count = self.studies_count

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "studiesCount": studies_count,
                "value": value,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        studies_count = d.pop("studiesCount")

        value = d.pop("value")

        value_count = cls(
            studies_count=studies_count,
            value=value,
        )

        return value_count
