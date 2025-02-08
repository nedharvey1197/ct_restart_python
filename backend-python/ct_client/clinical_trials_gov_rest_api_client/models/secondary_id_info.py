from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.secondary_id_type import SecondaryIdType
from ..types import UNSET, Unset

T = TypeVar("T", bound="SecondaryIdInfo")


@_attrs_define
class SecondaryIdInfo:
    """
    Attributes:
        id (Union[Unset, str]):
        type_ (Union[Unset, SecondaryIdType]):
        domain (Union[Unset, str]):
        link (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    type_: Union[Unset, SecondaryIdType] = UNSET
    domain: Union[Unset, str] = UNSET
    link: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        domain = self.domain

        link = self.link

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if domain is not UNSET:
            field_dict["domain"] = domain
        if link is not UNSET:
            field_dict["link"] = link

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, SecondaryIdType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = SecondaryIdType(_type_)

        domain = d.pop("domain", UNSET)

        link = d.pop("link", UNSET)

        secondary_id_info = cls(
            id=id,
            type_=type_,
            domain=domain,
            link=link,
        )

        secondary_id_info.additional_properties = d
        return secondary_id_info

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
