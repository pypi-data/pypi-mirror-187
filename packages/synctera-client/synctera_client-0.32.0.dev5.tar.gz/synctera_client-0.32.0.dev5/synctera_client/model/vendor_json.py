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


class VendorJson(
    schemas.AnyTypeSchema,
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "content_type",
            "vendor",
            "json",
        }
        
        class properties:
            
            
            class content_type(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "application/json": "APPLICATION_JSON",
                    }
                
                @schemas.classproperty
                def APPLICATION_JSON(cls):
                    return cls("application/json")
            json = schemas.DictSchema
            vendor = schemas.StrSchema
            __annotations__ = {
                "content_type": content_type,
                "json": json,
                "vendor": vendor,
            }

    
    content_type: MetaOapg.properties.content_type
    vendor: MetaOapg.properties.vendor
    json: MetaOapg.properties.json
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["content_type"]) -> MetaOapg.properties.content_type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["json"]) -> MetaOapg.properties.json: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["vendor"]) -> MetaOapg.properties.vendor: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["content_type", "json", "vendor", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["content_type"]) -> MetaOapg.properties.content_type: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["json"]) -> MetaOapg.properties.json: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["vendor"]) -> MetaOapg.properties.vendor: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["content_type", "json", "vendor", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
        content_type: typing.Union[MetaOapg.properties.content_type, str, ],
        vendor: typing.Union[MetaOapg.properties.vendor, str, ],
        json: typing.Union[MetaOapg.properties.json, dict, frozendict.frozendict, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'VendorJson':
        return super().__new__(
            cls,
            *_args,
            content_type=content_type,
            vendor=vendor,
            json=json,
            _configuration=_configuration,
            **kwargs,
        )
