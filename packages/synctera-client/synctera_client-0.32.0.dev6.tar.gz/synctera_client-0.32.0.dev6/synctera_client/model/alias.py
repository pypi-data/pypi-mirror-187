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


class Alias(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            account_id = schemas.UUIDSchema
            account_number = schemas.StrSchema
            alias_info = schemas.DictSchema
            alias_name = schemas.StrSchema
            alias_source = schemas.StrSchema
            alias_type = schemas.StrSchema
            id = schemas.UUIDSchema
            __annotations__ = {
                "account_id": account_id,
                "account_number": account_number,
                "alias_info": alias_info,
                "alias_name": alias_name,
                "alias_source": alias_source,
                "alias_type": alias_type,
                "id": id,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_id"]) -> MetaOapg.properties.account_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_number"]) -> MetaOapg.properties.account_number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["alias_info"]) -> MetaOapg.properties.alias_info: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["alias_name"]) -> MetaOapg.properties.alias_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["alias_source"]) -> MetaOapg.properties.alias_source: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["alias_type"]) -> MetaOapg.properties.alias_type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["account_id", "account_number", "alias_info", "alias_name", "alias_source", "alias_type", "id", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_id"]) -> typing.Union[MetaOapg.properties.account_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_number"]) -> typing.Union[MetaOapg.properties.account_number, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["alias_info"]) -> typing.Union[MetaOapg.properties.alias_info, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["alias_name"]) -> typing.Union[MetaOapg.properties.alias_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["alias_source"]) -> typing.Union[MetaOapg.properties.alias_source, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["alias_type"]) -> typing.Union[MetaOapg.properties.alias_type, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["account_id", "account_number", "alias_info", "alias_name", "alias_source", "alias_type", "id", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        account_id: typing.Union[MetaOapg.properties.account_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        account_number: typing.Union[MetaOapg.properties.account_number, str, schemas.Unset] = schemas.unset,
        alias_info: typing.Union[MetaOapg.properties.alias_info, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        alias_name: typing.Union[MetaOapg.properties.alias_name, str, schemas.Unset] = schemas.unset,
        alias_source: typing.Union[MetaOapg.properties.alias_source, str, schemas.Unset] = schemas.unset,
        alias_type: typing.Union[MetaOapg.properties.alias_type, str, schemas.Unset] = schemas.unset,
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Alias':
        return super().__new__(
            cls,
            *_args,
            account_id=account_id,
            account_number=account_number,
            alias_info=alias_info,
            alias_name=alias_name,
            alias_source=alias_source,
            alias_type=alias_type,
            id=id,
            _configuration=_configuration,
            **kwargs,
        )
