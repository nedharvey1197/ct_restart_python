from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.web_link import WebLink


T = TypeVar("T", bound="FieldNode")


@_attrs_define
class FieldNode:
    """
    Attributes:
        name (str):
        piece (str):
        source_type (str):
        type_ (str):
        alt_piece_names (Union[Unset, list[str]]):
        children (Union[Unset, list['FieldNode']]):
        ded_link (Union[Unset, WebLink]):
        description (Union[Unset, str]):
        historic_only (Union[Unset, bool]):
        indexed_only (Union[Unset, bool]):
        is_enum (Union[Unset, bool]):
        max_chars (Union[Unset, int]):
        nested (Union[Unset, bool]):
        rules (Union[Unset, str]):
        synonyms (Union[Unset, bool]):
        title (Union[Unset, str]):
    """

    name: str
    piece: str
    source_type: str
    type_: str
    alt_piece_names: Union[Unset, list[str]] = UNSET
    children: Union[Unset, list["FieldNode"]] = UNSET
    ded_link: Union[Unset, "WebLink"] = UNSET
    description: Union[Unset, str] = UNSET
    historic_only: Union[Unset, bool] = UNSET
    indexed_only: Union[Unset, bool] = UNSET
    is_enum: Union[Unset, bool] = UNSET
    max_chars: Union[Unset, int] = UNSET
    nested: Union[Unset, bool] = UNSET
    rules: Union[Unset, str] = UNSET
    synonyms: Union[Unset, bool] = UNSET
    title: Union[Unset, str] = UNSET

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        piece = self.piece

        source_type = self.source_type

        type_ = self.type_

        alt_piece_names: Union[Unset, list[str]] = UNSET
        if not isinstance(self.alt_piece_names, Unset):
            alt_piece_names = self.alt_piece_names

        children: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = children_item_data.to_dict()
                children.append(children_item)

        ded_link: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.ded_link, Unset):
            ded_link = self.ded_link.to_dict()

        description = self.description

        historic_only = self.historic_only

        indexed_only = self.indexed_only

        is_enum = self.is_enum

        max_chars = self.max_chars

        nested = self.nested

        rules = self.rules

        synonyms = self.synonyms

        title = self.title

        field_dict: dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
                "piece": piece,
                "sourceType": source_type,
                "type": type_,
            }
        )
        if alt_piece_names is not UNSET:
            field_dict["altPieceNames"] = alt_piece_names
        if children is not UNSET:
            field_dict["children"] = children
        if ded_link is not UNSET:
            field_dict["dedLink"] = ded_link
        if description is not UNSET:
            field_dict["description"] = description
        if historic_only is not UNSET:
            field_dict["historicOnly"] = historic_only
        if indexed_only is not UNSET:
            field_dict["indexedOnly"] = indexed_only
        if is_enum is not UNSET:
            field_dict["isEnum"] = is_enum
        if max_chars is not UNSET:
            field_dict["maxChars"] = max_chars
        if nested is not UNSET:
            field_dict["nested"] = nested
        if rules is not UNSET:
            field_dict["rules"] = rules
        if synonyms is not UNSET:
            field_dict["synonyms"] = synonyms
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.web_link import WebLink

        d = src_dict.copy()
        name = d.pop("name")

        piece = d.pop("piece")

        source_type = d.pop("sourceType")

        type_ = d.pop("type")

        alt_piece_names = cast(list[str], d.pop("altPieceNames", UNSET))

        children = []
        _children = d.pop("children", UNSET)
        for children_item_data in _children or []:
            children_item = FieldNode.from_dict(children_item_data)

            children.append(children_item)

        _ded_link = d.pop("dedLink", UNSET)
        ded_link: Union[Unset, WebLink]
        if isinstance(_ded_link, Unset):
            ded_link = UNSET
        else:
            ded_link = WebLink.from_dict(_ded_link)

        description = d.pop("description", UNSET)

        historic_only = d.pop("historicOnly", UNSET)

        indexed_only = d.pop("indexedOnly", UNSET)

        is_enum = d.pop("isEnum", UNSET)

        max_chars = d.pop("maxChars", UNSET)

        nested = d.pop("nested", UNSET)

        rules = d.pop("rules", UNSET)

        synonyms = d.pop("synonyms", UNSET)

        title = d.pop("title", UNSET)

        field_node = cls(
            name=name,
            piece=piece,
            source_type=source_type,
            type_=type_,
            alt_piece_names=alt_piece_names,
            children=children,
            ded_link=ded_link,
            description=description,
            historic_only=historic_only,
            indexed_only=indexed_only,
            is_enum=is_enum,
            max_chars=max_chars,
            nested=nested,
            rules=rules,
            synonyms=synonyms,
            title=title,
        )

        return field_node
