from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.fetch_study_format import FetchStudyFormat
from ...models.fetch_study_markup_format import FetchStudyMarkupFormat
from ...types import UNSET, Response, Unset


def _get_kwargs(
    nct_id: str,
    *,
    format_: Union[Unset, FetchStudyFormat] = FetchStudyFormat.JSON,
    markup_format: Union[Unset, FetchStudyMarkupFormat] = FetchStudyMarkupFormat.MARKDOWN,
    fields: Union[Unset, list[str]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_format_: Union[Unset, str] = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value

    params["format"] = json_format_

    json_markup_format: Union[Unset, str] = UNSET
    if not isinstance(markup_format, Unset):
        json_markup_format = markup_format.value

    params["markupFormat"] = json_markup_format

    json_fields: Union[Unset, list[str]] = UNSET
    if not isinstance(fields, Unset):
        json_fields = fields

    params["fields"] = json_fields

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/studies/{nct_id}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, str]]:
    if response.status_code == 200:
        response_200 = response.text
        return response_200
    if response.status_code == 301:
        response_301 = cast(Any, None)
        return response_301
    if response.status_code == 400:
        response_400 = response.text
        return response_400
    if response.status_code == 404:
        response_404 = response.text
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, str]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    nct_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    format_: Union[Unset, FetchStudyFormat] = FetchStudyFormat.JSON,
    markup_format: Union[Unset, FetchStudyMarkupFormat] = FetchStudyMarkupFormat.MARKDOWN,
    fields: Union[Unset, list[str]] = UNSET,
) -> Response[Union[Any, str]]:
    """Single Study

     Returns data of a single study.

    Args:
        nct_id (str):
        format_ (Union[Unset, FetchStudyFormat]):  Default: FetchStudyFormat.JSON.
        markup_format (Union[Unset, FetchStudyMarkupFormat]):  Default:
            FetchStudyMarkupFormat.MARKDOWN.
        fields (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, str]]
    """

    kwargs = _get_kwargs(
        nct_id=nct_id,
        format_=format_,
        markup_format=markup_format,
        fields=fields,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    nct_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    format_: Union[Unset, FetchStudyFormat] = FetchStudyFormat.JSON,
    markup_format: Union[Unset, FetchStudyMarkupFormat] = FetchStudyMarkupFormat.MARKDOWN,
    fields: Union[Unset, list[str]] = UNSET,
) -> Optional[Union[Any, str]]:
    """Single Study

     Returns data of a single study.

    Args:
        nct_id (str):
        format_ (Union[Unset, FetchStudyFormat]):  Default: FetchStudyFormat.JSON.
        markup_format (Union[Unset, FetchStudyMarkupFormat]):  Default:
            FetchStudyMarkupFormat.MARKDOWN.
        fields (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, str]
    """

    return sync_detailed(
        nct_id=nct_id,
        client=client,
        format_=format_,
        markup_format=markup_format,
        fields=fields,
    ).parsed


async def asyncio_detailed(
    nct_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    format_: Union[Unset, FetchStudyFormat] = FetchStudyFormat.JSON,
    markup_format: Union[Unset, FetchStudyMarkupFormat] = FetchStudyMarkupFormat.MARKDOWN,
    fields: Union[Unset, list[str]] = UNSET,
) -> Response[Union[Any, str]]:
    """Single Study

     Returns data of a single study.

    Args:
        nct_id (str):
        format_ (Union[Unset, FetchStudyFormat]):  Default: FetchStudyFormat.JSON.
        markup_format (Union[Unset, FetchStudyMarkupFormat]):  Default:
            FetchStudyMarkupFormat.MARKDOWN.
        fields (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, str]]
    """

    kwargs = _get_kwargs(
        nct_id=nct_id,
        format_=format_,
        markup_format=markup_format,
        fields=fields,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    nct_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
    format_: Union[Unset, FetchStudyFormat] = FetchStudyFormat.JSON,
    markup_format: Union[Unset, FetchStudyMarkupFormat] = FetchStudyMarkupFormat.MARKDOWN,
    fields: Union[Unset, list[str]] = UNSET,
) -> Optional[Union[Any, str]]:
    """Single Study

     Returns data of a single study.

    Args:
        nct_id (str):
        format_ (Union[Unset, FetchStudyFormat]):  Default: FetchStudyFormat.JSON.
        markup_format (Union[Unset, FetchStudyMarkupFormat]):  Default:
            FetchStudyMarkupFormat.MARKDOWN.
        fields (Union[Unset, list[str]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, str]
    """

    return (
        await asyncio_detailed(
            nct_id=nct_id,
            client=client,
            format_=format_,
            markup_format=markup_format,
            fields=fields,
        )
    ).parsed
