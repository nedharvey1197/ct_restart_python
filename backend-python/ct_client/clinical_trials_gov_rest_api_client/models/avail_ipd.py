from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AvailIpd")


@_attrs_define
class AvailIpd:
    """
    Attributes:
        id (Union[Unset, str]):
        type_ (Union[Unset, str]):
        url (Union[Unset, str]):
        comment (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        url = self.url

        comment = self.comment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if url is not UNSET:
            field_dict["url"] = url
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        type_ = d.pop("type", UNSET)

        url = d.pop("url", UNSET)

        comment = d.pop("comment", UNSET)

        avail_ipd = cls(
            id=id,
            type_=type_,
            url=url,
            comment=comment,
        )

        avail_ipd.additional_properties = d
        return avail_ipd

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
