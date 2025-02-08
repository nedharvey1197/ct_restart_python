from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.reference_type import ReferenceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.retraction import Retraction


T = TypeVar("T", bound="Reference")


@_attrs_define
class Reference:
    """
    Attributes:
        pmid (Union[Unset, str]):
        type_ (Union[Unset, ReferenceType]):
        citation (Union[Unset, str]):
        retractions (Union[Unset, list['Retraction']]):
    """

    pmid: Union[Unset, str] = UNSET
    type_: Union[Unset, ReferenceType] = UNSET
    citation: Union[Unset, str] = UNSET
    retractions: Union[Unset, list["Retraction"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pmid = self.pmid

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        citation = self.citation

        retractions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.retractions, Unset):
            retractions = []
            for retractions_item_data in self.retractions:
                retractions_item = retractions_item_data.to_dict()
                retractions.append(retractions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pmid is not UNSET:
            field_dict["pmid"] = pmid
        if type_ is not UNSET:
            field_dict["type"] = type_
        if citation is not UNSET:
            field_dict["citation"] = citation
        if retractions is not UNSET:
            field_dict["retractions"] = retractions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.retraction import Retraction

        d = src_dict.copy()
        pmid = d.pop("pmid", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, ReferenceType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ReferenceType(_type_)

        citation = d.pop("citation", UNSET)

        retractions = []
        _retractions = d.pop("retractions", UNSET)
        for retractions_item_data in _retractions or []:
            retractions_item = Retraction.from_dict(retractions_item_data)

            retractions.append(retractions_item)

        reference = cls(
            pmid=pmid,
            type_=type_,
            citation=citation,
            retractions=retractions,
        )

        reference.additional_properties = d
        return reference

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
