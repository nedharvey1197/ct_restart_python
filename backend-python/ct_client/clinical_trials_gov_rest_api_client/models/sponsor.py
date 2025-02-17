from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.agency_class import AgencyClass
from ..types import UNSET, Unset

T = TypeVar("T", bound="Sponsor")


@_attrs_define
class Sponsor:
    """
    Attributes:
        name (Union[Unset, str]):
        class_ (Union[Unset, AgencyClass]):
    """

    name: Union[Unset, str] = UNSET
    class_: Union[Unset, AgencyClass] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        class_: Union[Unset, str] = UNSET
        if not isinstance(self.class_, Unset):
            class_ = self.class_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if class_ is not UNSET:
            field_dict["class"] = class_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        _class_ = d.pop("class", UNSET)
        class_: Union[Unset, AgencyClass]
        if isinstance(_class_, Unset):
            class_ = UNSET
        else:
            class_ = AgencyClass(_class_)

        sponsor = cls(
            name=name,
            class_=class_,
        )

        sponsor.additional_properties = d
        return sponsor

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
