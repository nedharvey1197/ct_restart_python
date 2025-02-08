from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ConditionsModule")


@_attrs_define
class ConditionsModule:
    """
    Attributes:
        conditions (Union[Unset, list[str]]):
        keywords (Union[Unset, list[str]]):
    """

    conditions: Union[Unset, list[str]] = UNSET
    keywords: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        conditions: Union[Unset, list[str]] = UNSET
        if not isinstance(self.conditions, Unset):
            conditions = self.conditions

        keywords: Union[Unset, list[str]] = UNSET
        if not isinstance(self.keywords, Unset):
            keywords = self.keywords

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if conditions is not UNSET:
            field_dict["conditions"] = conditions
        if keywords is not UNSET:
            field_dict["keywords"] = keywords

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        conditions = cast(list[str], d.pop("conditions", UNSET))

        keywords = cast(list[str], d.pop("keywords", UNSET))

        conditions_module = cls(
            conditions=conditions,
            keywords=keywords,
        )

        conditions_module.additional_properties = d
        return conditions_module

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
