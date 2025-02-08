from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.search_area import SearchArea


T = TypeVar("T", bound="SearchDocument")


@_attrs_define
class SearchDocument:
    """
    Attributes:
        areas (list['SearchArea']):
        name (str):
    """

    areas: list["SearchArea"]
    name: str

    def to_dict(self) -> dict[str, Any]:
        areas = []
        for areas_item_data in self.areas:
            areas_item = areas_item_data.to_dict()
            areas.append(areas_item)

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "areas": areas,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_area import SearchArea

        d = src_dict.copy()
        areas = []
        _areas = d.pop("areas")
        for areas_item_data in _areas:
            areas_item = SearchArea.from_dict(areas_item_data)

            areas.append(areas_item)

        name = d.pop("name")

        search_document = cls(
            areas=areas,
            name=name,
        )

        return search_document
