from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.enrollment_type import EnrollmentType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EnrollmentInfo")


@_attrs_define
class EnrollmentInfo:
    """
    Attributes:
        count (Union[Unset, int]):
        type_ (Union[Unset, EnrollmentType]):
    """

    count: Union[Unset, int] = UNSET
    type_: Union[Unset, EnrollmentType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        count = self.count

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if count is not UNSET:
            field_dict["count"] = count
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        count = d.pop("count", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, EnrollmentType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = EnrollmentType(_type_)

        enrollment_info = cls(
            count=count,
            type_=type_,
        )

        enrollment_info.additional_properties = d
        return enrollment_info

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
