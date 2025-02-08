from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.flow_stats import FlowStats


T = TypeVar("T", bound="FlowMilestone")


@_attrs_define
class FlowMilestone:
    """
    Attributes:
        type_ (Union[Unset, str]):
        comment (Union[Unset, str]):
        achievements (Union[Unset, list['FlowStats']]):
    """

    type_: Union[Unset, str] = UNSET
    comment: Union[Unset, str] = UNSET
    achievements: Union[Unset, list["FlowStats"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        comment = self.comment

        achievements: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.achievements, Unset):
            achievements = []
            for achievements_item_data in self.achievements:
                achievements_item = achievements_item_data.to_dict()
                achievements.append(achievements_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if comment is not UNSET:
            field_dict["comment"] = comment
        if achievements is not UNSET:
            field_dict["achievements"] = achievements

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.flow_stats import FlowStats

        d = src_dict.copy()
        type_ = d.pop("type", UNSET)

        comment = d.pop("comment", UNSET)

        achievements = []
        _achievements = d.pop("achievements", UNSET)
        for achievements_item_data in _achievements or []:
            achievements_item = FlowStats.from_dict(achievements_item_data)

            achievements.append(achievements_item)

        flow_milestone = cls(
            type_=type_,
            comment=comment,
            achievements=achievements,
        )

        flow_milestone.additional_properties = d
        return flow_milestone

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
