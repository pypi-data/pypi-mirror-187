# coding: utf-8

"""
    Synctera API

    <h2>Let's build something great.</h2><p>Welcome to the official reference documentation for Synctera APIs. Our APIs are the best way to automate your company's banking needs and are designed to be easy to understand and implement.</p><p>We're continuously growing this library and what you see here is just the start, but if you need something specific or have a question, <a class='text-blue-600' href='https://synctera.com/contact' target='_blank' rel='noreferrer'>contact us</a>.</p>   # noqa: E501

    The version of the OpenAPI document: 0.32.0.dev5
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from synctera_client import schemas  # noqa: F401


class UpdateCardImageRequest(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "status",
        }
        
        class properties:
        
            @staticmethod
            def status() -> typing.Type['CardImageStatus']:
                return CardImageStatus
            rejection_memo = schemas.StrSchema
        
            @staticmethod
            def rejection_reason() -> typing.Type['CardImageRejectionReason']:
                return CardImageRejectionReason
            __annotations__ = {
                "status": status,
                "rejection_memo": rejection_memo,
                "rejection_reason": rejection_reason,
            }
    
    status: 'CardImageStatus'
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> 'CardImageStatus': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["rejection_memo"]) -> MetaOapg.properties.rejection_memo: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["rejection_reason"]) -> 'CardImageRejectionReason': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["status", "rejection_memo", "rejection_reason", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> 'CardImageStatus': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["rejection_memo"]) -> typing.Union[MetaOapg.properties.rejection_memo, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["rejection_reason"]) -> typing.Union['CardImageRejectionReason', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["status", "rejection_memo", "rejection_reason", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        status: 'CardImageStatus',
        rejection_memo: typing.Union[MetaOapg.properties.rejection_memo, str, schemas.Unset] = schemas.unset,
        rejection_reason: typing.Union['CardImageRejectionReason', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'UpdateCardImageRequest':
        return super().__new__(
            cls,
            *_args,
            status=status,
            rejection_memo=rejection_memo,
            rejection_reason=rejection_reason,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.card_image_rejection_reason import CardImageRejectionReason
from synctera_client.model.card_image_status import CardImageStatus
