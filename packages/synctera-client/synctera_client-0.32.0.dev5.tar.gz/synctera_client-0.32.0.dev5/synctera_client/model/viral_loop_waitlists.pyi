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


class ViralLoopWaitlists(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Viral Loop Waitlists
    """


    class MetaOapg:
        required = {
            "viral_loop_api_token",
            "id",
        }
        
        class properties:
            id = schemas.UUIDSchema
            
            
            class viral_loop_api_token(
                schemas.StrSchema
            ):
                pass
            bank_id = schemas.IntSchema
            creation_time = schemas.DateTimeSchema
            last_updated_time = schemas.DateTimeSchema
            
            
            class lead_count(
                schemas.IntSchema
            ):
                pass
            partner_id = schemas.IntSchema
            __annotations__ = {
                "id": id,
                "viral_loop_api_token": viral_loop_api_token,
                "bank_id": bank_id,
                "creation_time": creation_time,
                "last_updated_time": last_updated_time,
                "lead_count": lead_count,
                "partner_id": partner_id,
            }
    
    viral_loop_api_token: MetaOapg.properties.viral_loop_api_token
    id: MetaOapg.properties.id
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["viral_loop_api_token"]) -> MetaOapg.properties.viral_loop_api_token: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bank_id"]) -> MetaOapg.properties.bank_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["lead_count"]) -> MetaOapg.properties.lead_count: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["partner_id"]) -> MetaOapg.properties.partner_id: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "viral_loop_api_token", "bank_id", "creation_time", "last_updated_time", "lead_count", "partner_id", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["viral_loop_api_token"]) -> MetaOapg.properties.viral_loop_api_token: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bank_id"]) -> typing.Union[MetaOapg.properties.bank_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["creation_time"]) -> typing.Union[MetaOapg.properties.creation_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_updated_time"]) -> typing.Union[MetaOapg.properties.last_updated_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["lead_count"]) -> typing.Union[MetaOapg.properties.lead_count, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["partner_id"]) -> typing.Union[MetaOapg.properties.partner_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "viral_loop_api_token", "bank_id", "creation_time", "last_updated_time", "lead_count", "partner_id", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        viral_loop_api_token: typing.Union[MetaOapg.properties.viral_loop_api_token, str, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        bank_id: typing.Union[MetaOapg.properties.bank_id, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        creation_time: typing.Union[MetaOapg.properties.creation_time, str, datetime, schemas.Unset] = schemas.unset,
        last_updated_time: typing.Union[MetaOapg.properties.last_updated_time, str, datetime, schemas.Unset] = schemas.unset,
        lead_count: typing.Union[MetaOapg.properties.lead_count, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        partner_id: typing.Union[MetaOapg.properties.partner_id, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ViralLoopWaitlists':
        return super().__new__(
            cls,
            *_args,
            viral_loop_api_token=viral_loop_api_token,
            id=id,
            bank_id=bank_id,
            creation_time=creation_time,
            last_updated_time=last_updated_time,
            lead_count=lead_count,
            partner_id=partner_id,
            _configuration=_configuration,
            **kwargs,
        )
