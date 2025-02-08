from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.recruitment_status import RecruitmentStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.contact import Contact
    from ..models.geo_point import GeoPoint


T = TypeVar("T", bound="Location")


@_attrs_define
class Location:
    """
    Attributes:
        facility (Union[Unset, str]):
        status (Union[Unset, RecruitmentStatus]):
        city (Union[Unset, str]):
        state (Union[Unset, str]):
        zip_ (Union[Unset, str]):
        country (Union[Unset, str]):
        contacts (Union[Unset, list['Contact']]):
        country_code (Union[Unset, str]):
        geo_point (Union[Unset, GeoPoint]):
    """

    facility: Union[Unset, str] = UNSET
    status: Union[Unset, RecruitmentStatus] = UNSET
    city: Union[Unset, str] = UNSET
    state: Union[Unset, str] = UNSET
    zip_: Union[Unset, str] = UNSET
    country: Union[Unset, str] = UNSET
    contacts: Union[Unset, list["Contact"]] = UNSET
    country_code: Union[Unset, str] = UNSET
    geo_point: Union[Unset, "GeoPoint"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        facility = self.facility

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        city = self.city

        state = self.state

        zip_ = self.zip_

        country = self.country

        contacts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.contacts, Unset):
            contacts = []
            for contacts_item_data in self.contacts:
                contacts_item = contacts_item_data.to_dict()
                contacts.append(contacts_item)

        country_code = self.country_code

        geo_point: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.geo_point, Unset):
            geo_point = self.geo_point.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if facility is not UNSET:
            field_dict["facility"] = facility
        if status is not UNSET:
            field_dict["status"] = status
        if city is not UNSET:
            field_dict["city"] = city
        if state is not UNSET:
            field_dict["state"] = state
        if zip_ is not UNSET:
            field_dict["zip"] = zip_
        if country is not UNSET:
            field_dict["country"] = country
        if contacts is not UNSET:
            field_dict["contacts"] = contacts
        if country_code is not UNSET:
            field_dict["countryCode"] = country_code
        if geo_point is not UNSET:
            field_dict["geoPoint"] = geo_point

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.contact import Contact
        from ..models.geo_point import GeoPoint

        d = src_dict.copy()
        facility = d.pop("facility", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, RecruitmentStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = RecruitmentStatus(_status)

        city = d.pop("city", UNSET)

        state = d.pop("state", UNSET)

        zip_ = d.pop("zip", UNSET)

        country = d.pop("country", UNSET)

        contacts = []
        _contacts = d.pop("contacts", UNSET)
        for contacts_item_data in _contacts or []:
            contacts_item = Contact.from_dict(contacts_item_data)

            contacts.append(contacts_item)

        country_code = d.pop("countryCode", UNSET)

        _geo_point = d.pop("geoPoint", UNSET)
        geo_point: Union[Unset, GeoPoint]
        if isinstance(_geo_point, Unset):
            geo_point = UNSET
        else:
            geo_point = GeoPoint.from_dict(_geo_point)

        location = cls(
            facility=facility,
            status=status,
            city=city,
            state=state,
            zip_=zip_,
            country=country,
            contacts=contacts,
            country_code=country_code,
            geo_point=geo_point,
        )

        location.additional_properties = d
        return location

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
