from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.violation_event import ViolationEvent


T = TypeVar("T", bound="ViolationAnnotation")


@_attrs_define
class ViolationAnnotation:
    """
    Attributes:
        violation_events (Union[Unset, list['ViolationEvent']]):
    """

    violation_events: Union[Unset, list["ViolationEvent"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        violation_events: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.violation_events, Unset):
            violation_events = []
            for violation_events_item_data in self.violation_events:
                violation_events_item = violation_events_item_data.to_dict()
                violation_events.append(violation_events_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if violation_events is not UNSET:
            field_dict["violationEvents"] = violation_events

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.violation_event import ViolationEvent

        d = src_dict.copy()
        violation_events = []
        _violation_events = d.pop("violationEvents", UNSET)
        for violation_events_item_data in _violation_events or []:
            violation_events_item = ViolationEvent.from_dict(violation_events_item_data)

            violation_events.append(violation_events_item)

        violation_annotation = cls(
            violation_events=violation_events,
        )

        violation_annotation.additional_properties = d
        return violation_annotation

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
