import datetime
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.unposted_event_type import UnpostedEventType
from ..types import UNSET, Unset

T = TypeVar("T", bound="UnpostedEvent")


@_attrs_define
class UnpostedEvent:
    """
    Attributes:
        type_ (Union[Unset, UnpostedEventType]):
        date (Union[Unset, datetime.date]):
        date_unknown (Union[Unset, bool]):
    """

    type_: Union[Unset, UnpostedEventType] = UNSET
    date: Union[Unset, datetime.date] = UNSET
    date_unknown: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        date_unknown = self.date_unknown

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if date is not UNSET:
            field_dict["date"] = date
        if date_unknown is not UNSET:
            field_dict["dateUnknown"] = date_unknown

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, UnpostedEventType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = UnpostedEventType(_type_)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        date_unknown = d.pop("dateUnknown", UNSET)

        unposted_event = cls(
            type_=type_,
            date=date,
            date_unknown=date_unknown,
        )

        unposted_event.additional_properties = d
        return unposted_event

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
