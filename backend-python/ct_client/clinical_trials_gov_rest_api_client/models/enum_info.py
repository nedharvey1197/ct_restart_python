from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.enum_item import EnumItem


T = TypeVar("T", bound="EnumInfo")


@_attrs_define
class EnumInfo:
    """
    Attributes:
        pieces (list[str]):
        type_ (str):
        values (list['EnumItem']):
    """

    pieces: list[str]
    type_: str
    values: list["EnumItem"]

    def to_dict(self) -> dict[str, Any]:
        pieces = self.pieces

        type_ = self.type_

        values = []
        for values_item_data in self.values:
            values_item = values_item_data.to_dict()
            values.append(values_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "pieces": pieces,
                "type": type_,
                "values": values,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.enum_item import EnumItem

        d = src_dict.copy()
        pieces = cast(list[str], d.pop("pieces"))

        type_ = d.pop("type")

        values = []
        _values = d.pop("values")
        for values_item_data in _values:
            values_item = EnumItem.from_dict(values_item_data)

            values.append(values_item)

        enum_info = cls(
            pieces=pieces,
            type_=type_,
            values=values,
        )

        return enum_info
