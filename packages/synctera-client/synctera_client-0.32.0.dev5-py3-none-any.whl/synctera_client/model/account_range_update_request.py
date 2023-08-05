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


class AccountRangeUpdateRequest(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            end_date = schemas.DateTimeSchema
            is_tokenization_enabled = schemas.BoolSchema
        
            @staticmethod
            def physical_card_format() -> typing.Type['PhysicalCardFormat']:
                return PhysicalCardFormat
            start_date = schemas.DateTimeSchema
            __annotations__ = {
                "end_date": end_date,
                "is_tokenization_enabled": is_tokenization_enabled,
                "physical_card_format": physical_card_format,
                "start_date": start_date,
            }
        additional_properties = schemas.NotAnyTypeSchema
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["end_date"]) -> MetaOapg.properties.end_date: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_tokenization_enabled"]) -> MetaOapg.properties.is_tokenization_enabled: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["physical_card_format"]) -> 'PhysicalCardFormat': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["start_date"]) -> MetaOapg.properties.start_date: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["end_date"], typing_extensions.Literal["is_tokenization_enabled"], typing_extensions.Literal["physical_card_format"], typing_extensions.Literal["start_date"], ]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["end_date"]) -> typing.Union[MetaOapg.properties.end_date, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_tokenization_enabled"]) -> typing.Union[MetaOapg.properties.is_tokenization_enabled, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["physical_card_format"]) -> typing.Union['PhysicalCardFormat', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["start_date"]) -> typing.Union[MetaOapg.properties.start_date, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["end_date"], typing_extensions.Literal["is_tokenization_enabled"], typing_extensions.Literal["physical_card_format"], typing_extensions.Literal["start_date"], ]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        end_date: typing.Union[MetaOapg.properties.end_date, str, datetime, schemas.Unset] = schemas.unset,
        is_tokenization_enabled: typing.Union[MetaOapg.properties.is_tokenization_enabled, bool, schemas.Unset] = schemas.unset,
        physical_card_format: typing.Union['PhysicalCardFormat', schemas.Unset] = schemas.unset,
        start_date: typing.Union[MetaOapg.properties.start_date, str, datetime, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'AccountRangeUpdateRequest':
        return super().__new__(
            cls,
            *_args,
            end_date=end_date,
            is_tokenization_enabled=is_tokenization_enabled,
            physical_card_format=physical_card_format,
            start_date=start_date,
            _configuration=_configuration,
        )

from synctera_client.model.physical_card_format import PhysicalCardFormat
