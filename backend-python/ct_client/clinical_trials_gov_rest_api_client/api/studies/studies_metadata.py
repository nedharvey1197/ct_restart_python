from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.field_node import FieldNode
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    include_indexed_only: Union[Unset, bool] = False,
    include_historic_only: Union[Unset, bool] = False,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["includeIndexedOnly"] = include_indexed_only

    params["includeHistoricOnly"] = include_historic_only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/studies/metadata",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[list["FieldNode"], str]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_field_node_list_item_data in _response_200:
            componentsschemas_field_node_list_item = FieldNode.from_dict(componentsschemas_field_node_list_item_data)

            response_200.append(componentsschemas_field_node_list_item)

        return response_200
    if response.status_code == 400:
        response_400 = response.text
        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[list["FieldNode"], str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    include_indexed_only: Union[Unset, bool] = False,
    include_historic_only: Union[Unset, bool] = False,
) -> Response[Union[list["FieldNode"], str]]:
    """Data Model Fields

     Returns study data model fields.

    Args:
        include_indexed_only (Union[Unset, bool]):  Default: False.
        include_historic_only (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[list['FieldNode'], str]]
    """

    kwargs = _get_kwargs(
        include_indexed_only=include_indexed_only,
        include_historic_only=include_historic_only,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    include_indexed_only: Union[Unset, bool] = False,
    include_historic_only: Union[Unset, bool] = False,
) -> Optional[Union[list["FieldNode"], str]]:
    """Data Model Fields

     Returns study data model fields.

    Args:
        include_indexed_only (Union[Unset, bool]):  Default: False.
        include_historic_only (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[list['FieldNode'], str]
    """

    return sync_detailed(
        client=client,
        include_indexed_only=include_indexed_only,
        include_historic_only=include_historic_only,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    include_indexed_only: Union[Unset, bool] = False,
    include_historic_only: Union[Unset, bool] = False,
) -> Response[Union[list["FieldNode"], str]]:
    """Data Model Fields

     Returns study data model fields.

    Args:
        include_indexed_only (Union[Unset, bool]):  Default: False.
        include_historic_only (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[list['FieldNode'], str]]
    """

    kwargs = _get_kwargs(
        include_indexed_only=include_indexed_only,
        include_historic_only=include_historic_only,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    include_indexed_only: Union[Unset, bool] = False,
    include_historic_only: Union[Unset, bool] = False,
) -> Optional[Union[list["FieldNode"], str]]:
    """Data Model Fields

     Returns study data model fields.

    Args:
        include_indexed_only (Union[Unset, bool]):  Default: False.
        include_historic_only (Union[Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[list['FieldNode'], str]
    """

    return (
        await asyncio_detailed(
            client=client,
            include_indexed_only=include_indexed_only,
            include_historic_only=include_historic_only,
        )
    ).parsed
