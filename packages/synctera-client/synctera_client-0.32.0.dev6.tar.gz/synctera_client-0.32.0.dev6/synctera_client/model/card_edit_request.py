# coding: utf-8

"""
    Synctera API

    <h2>Let's build something great.</h2><p>Welcome to the official reference documentation for Synctera APIs. Our APIs are the best way to automate your company's banking needs and are designed to be easy to understand and implement.</p><p>We're continuously growing this library and what you see here is just the start, but if you need something specific or have a question, <a class='text-blue-600' href='https://synctera.com/contact' target='_blank' rel='noreferrer'>contact us</a>.</p>   # noqa: E501

    The version of the OpenAPI document: 0.32.0.dev6
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


class CardEditRequest(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
        
            @staticmethod
            def card_status() -> typing.Type['CardStatusRequest']:
                return CardStatusRequest
            customer_id = schemas.UUIDSchema
        
            @staticmethod
            def emboss_name() -> typing.Type['EmbossName']:
                return EmbossName
        
            @staticmethod
            def memo() -> typing.Type['CardStatusReasonMemo']:
                return CardStatusReasonMemo
        
            @staticmethod
            def metadata() -> typing.Type['CardMetadata']:
                return CardMetadata
        
            @staticmethod
            def reason() -> typing.Type['CardStatusReasonCode']:
                return CardStatusReasonCode
            __annotations__ = {
                "card_status": card_status,
                "customer_id": customer_id,
                "emboss_name": emboss_name,
                "memo": memo,
                "metadata": metadata,
                "reason": reason,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["card_status"]) -> 'CardStatusRequest': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["customer_id"]) -> MetaOapg.properties.customer_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["emboss_name"]) -> 'EmbossName': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["memo"]) -> 'CardStatusReasonMemo': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> 'CardMetadata': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["reason"]) -> 'CardStatusReasonCode': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["card_status", "customer_id", "emboss_name", "memo", "metadata", "reason", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["card_status"]) -> typing.Union['CardStatusRequest', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["customer_id"]) -> typing.Union[MetaOapg.properties.customer_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["emboss_name"]) -> typing.Union['EmbossName', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["memo"]) -> typing.Union['CardStatusReasonMemo', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union['CardMetadata', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["reason"]) -> typing.Union['CardStatusReasonCode', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["card_status", "customer_id", "emboss_name", "memo", "metadata", "reason", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        card_status: typing.Union['CardStatusRequest', schemas.Unset] = schemas.unset,
        customer_id: typing.Union[MetaOapg.properties.customer_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        emboss_name: typing.Union['EmbossName', schemas.Unset] = schemas.unset,
        memo: typing.Union['CardStatusReasonMemo', schemas.Unset] = schemas.unset,
        metadata: typing.Union['CardMetadata', schemas.Unset] = schemas.unset,
        reason: typing.Union['CardStatusReasonCode', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CardEditRequest':
        return super().__new__(
            cls,
            *_args,
            card_status=card_status,
            customer_id=customer_id,
            emboss_name=emboss_name,
            memo=memo,
            metadata=metadata,
            reason=reason,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.card_metadata import CardMetadata
from synctera_client.model.card_status_reason_code import CardStatusReasonCode
from synctera_client.model.card_status_reason_memo import CardStatusReasonMemo
from synctera_client.model.card_status_request import CardStatusRequest
from synctera_client.model.emboss_name import EmbossName
