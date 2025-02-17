from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ListSize")


@_attrs_define
class ListSize:
    """
    Attributes:
        size (int):
        studies_count (int):
    """

    size: int
    studies_count: int

    def to_dict(self) -> dict[str, Any]:
        size = self.size

        studies_count = self.studies_count

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "size": size,
                "studiesCount": studies_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        size = d.pop("size")

        studies_count = d.pop("studiesCount")

        list_size = cls(
            size=size,
            studies_count=studies_count,
        )

        return list_size
