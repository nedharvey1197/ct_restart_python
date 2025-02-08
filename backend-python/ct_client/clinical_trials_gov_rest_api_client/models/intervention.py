from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.intervention_type import InterventionType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Intervention")


@_attrs_define
class Intervention:
    """
    Attributes:
        type_ (Union[Unset, InterventionType]):
        name (Union[Unset, str]):
        description (Union[Unset, str]):
        arm_group_labels (Union[Unset, list[str]]):
        other_names (Union[Unset, list[str]]):
    """

    type_: Union[Unset, InterventionType] = UNSET
    name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    arm_group_labels: Union[Unset, list[str]] = UNSET
    other_names: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        name = self.name

        description = self.description

        arm_group_labels: Union[Unset, list[str]] = UNSET
        if not isinstance(self.arm_group_labels, Unset):
            arm_group_labels = self.arm_group_labels

        other_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.other_names, Unset):
            other_names = self.other_names

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if name is not UNSET:
            field_dict["name"] = name
        if description is not UNSET:
            field_dict["description"] = description
        if arm_group_labels is not UNSET:
            field_dict["armGroupLabels"] = arm_group_labels
        if other_names is not UNSET:
            field_dict["otherNames"] = other_names

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, InterventionType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = InterventionType(_type_)

        name = d.pop("name", UNSET)

        description = d.pop("description", UNSET)

        arm_group_labels = cast(list[str], d.pop("armGroupLabels", UNSET))

        other_names = cast(list[str], d.pop("otherNames", UNSET))

        intervention = cls(
            type_=type_,
            name=name,
            description=description,
            arm_group_labels=arm_group_labels,
            other_names=other_names,
        )

        intervention.additional_properties = d
        return intervention

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
