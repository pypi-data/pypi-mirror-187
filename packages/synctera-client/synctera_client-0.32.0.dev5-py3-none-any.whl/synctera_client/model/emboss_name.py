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


class EmbossName(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    The customer details to emboss on the card - Defaults to customer first and last name. Is limited to 21 characters. Valid characters are A-Z, a-z, 0-9, space ( ), period (.), comma (,), forward slash (/), hyphen (-), ampersand (&), single quote (').
    """


    class MetaOapg:
        required = {
            "line_1",
        }
        
        class properties:
            line_1 = schemas.StrSchema
            line_2 = schemas.StrSchema
            __annotations__ = {
                "line_1": line_1,
                "line_2": line_2,
            }
    
    line_1: MetaOapg.properties.line_1
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["line_1"]) -> MetaOapg.properties.line_1: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["line_2"]) -> MetaOapg.properties.line_2: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["line_1", "line_2", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["line_1"]) -> MetaOapg.properties.line_1: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["line_2"]) -> typing.Union[MetaOapg.properties.line_2, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["line_1", "line_2", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        line_1: typing.Union[MetaOapg.properties.line_1, str, ],
        line_2: typing.Union[MetaOapg.properties.line_2, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'EmbossName':
        return super().__new__(
            cls,
            *_args,
            line_1=line_1,
            line_2=line_2,
            _configuration=_configuration,
            **kwargs,
        )
