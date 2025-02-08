from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.date_type import DateType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PartialDateStruct")


@_attrs_define
class PartialDateStruct:
    """
    Attributes:
        date (Union[Unset, str]): Date in `yyyy`, `yyyy-MM`, or `yyyy-MM-dd` format
        type_ (Union[Unset, DateType]):
    """

    date: Union[Unset, str] = UNSET
    type_: Union[Unset, DateType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if date is not UNSET:
            field_dict["date"] = date
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        date = d.pop("date", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, DateType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = DateType(_type_)

        partial_date_struct = cls(
            date=date,
            type_=type_,
        )

        partial_date_struct.additional_properties = d
        return partial_date_struct

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
