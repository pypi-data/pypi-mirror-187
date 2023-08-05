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


class BaseAccountVerification(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "vendor",
            "status",
        }
        
        class properties:
            
            
            class status(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "VERIFIED": "VERIFIED",
                        "UNVERIFIED": "UNVERIFIED",
                    }
                
                @schemas.classproperty
                def VERIFIED(cls):
                    return cls("VERIFIED")
                
                @schemas.classproperty
                def UNVERIFIED(cls):
                    return cls("UNVERIFIED")
            
            
            class vendor(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "PLAID": "PLAID",
                        "MANUAL": "MANUAL",
                        "FINICITY": "FINICITY",
                    }
                
                @schemas.classproperty
                def PLAID(cls):
                    return cls("PLAID")
                
                @schemas.classproperty
                def MANUAL(cls):
                    return cls("MANUAL")
                
                @schemas.classproperty
                def FINICITY(cls):
                    return cls("FINICITY")
            creation_time = schemas.DateTimeSchema
            last_updated_time = schemas.DateTimeSchema
            __annotations__ = {
                "status": status,
                "vendor": vendor,
                "creation_time": creation_time,
                "last_updated_time": last_updated_time,
            }
    
    vendor: MetaOapg.properties.vendor
    status: MetaOapg.properties.status
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["vendor"]) -> MetaOapg.properties.vendor: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["status", "vendor", "creation_time", "last_updated_time", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["vendor"]) -> MetaOapg.properties.vendor: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["creation_time"]) -> typing.Union[MetaOapg.properties.creation_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_updated_time"]) -> typing.Union[MetaOapg.properties.last_updated_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["status", "vendor", "creation_time", "last_updated_time", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        vendor: typing.Union[MetaOapg.properties.vendor, str, ],
        status: typing.Union[MetaOapg.properties.status, str, ],
        creation_time: typing.Union[MetaOapg.properties.creation_time, str, datetime, schemas.Unset] = schemas.unset,
        last_updated_time: typing.Union[MetaOapg.properties.last_updated_time, str, datetime, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'BaseAccountVerification':
        return super().__new__(
            cls,
            *_args,
            vendor=vendor,
            status=status,
            creation_time=creation_time,
            last_updated_time=last_updated_time,
            _configuration=_configuration,
            **kwargs,
        )
