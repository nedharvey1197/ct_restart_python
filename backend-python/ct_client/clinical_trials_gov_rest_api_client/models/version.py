from typing import Any, TypeVar, Union

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="Version")


@_attrs_define
class Version:
    """
    Attributes:
        api_version (str):
        data_timestamp (Union[Unset, str]):
    """

    api_version: str
    data_timestamp: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        api_version = self.api_version

        data_timestamp = self.data_timestamp

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "apiVersion": api_version,
            }
        )
        if data_timestamp is not UNSET:
            field_dict["dataTimestamp"] = data_timestamp

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        api_version = d.pop("apiVersion")

        data_timestamp = d.pop("dataTimestamp", UNSET)

        version = cls(
            api_version=api_version,
            data_timestamp=data_timestamp,
        )

        return version
