from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.arm_group_type import ArmGroupType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ArmGroup")


@_attrs_define
class ArmGroup:
    """
    Attributes:
        label (Union[Unset, str]):
        type_ (Union[Unset, ArmGroupType]):
        description (Union[Unset, str]):
        intervention_names (Union[Unset, list[str]]):
    """

    label: Union[Unset, str] = UNSET
    type_: Union[Unset, ArmGroupType] = UNSET
    description: Union[Unset, str] = UNSET
    intervention_names: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        description = self.description

        intervention_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.intervention_names, Unset):
            intervention_names = self.intervention_names

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if label is not UNSET:
            field_dict["label"] = label
        if type_ is not UNSET:
            field_dict["type"] = type_
        if description is not UNSET:
            field_dict["description"] = description
        if intervention_names is not UNSET:
            field_dict["interventionNames"] = intervention_names

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        label = d.pop("label", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, ArmGroupType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ArmGroupType(_type_)

        description = d.pop("description", UNSET)

        intervention_names = cast(list[str], d.pop("interventionNames", UNSET))

        arm_group = cls(
            label=label,
            type_=type_,
            description=description,
            intervention_names=intervention_names,
        )

        arm_group.additional_properties = d
        return arm_group

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
