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


class WatchlistSuppress(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "provider_subject_id",
            "provider_subscription_id",
            "status",
        }
        
        class properties:
            provider_subject_id = schemas.StrSchema
            provider_subscription_id = schemas.StrSchema
            
            
            class status(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def SUPPRESS(cls):
                    return cls("SUPPRESS")
                
                @schemas.classproperty
                def UNSUPPRESS(cls):
                    return cls("UNSUPPRESS")
            __annotations__ = {
                "provider_subject_id": provider_subject_id,
                "provider_subscription_id": provider_subscription_id,
                "status": status,
            }
    
    provider_subject_id: MetaOapg.properties.provider_subject_id
    provider_subscription_id: MetaOapg.properties.provider_subscription_id
    status: MetaOapg.properties.status
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["provider_subject_id"]) -> MetaOapg.properties.provider_subject_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["provider_subscription_id"]) -> MetaOapg.properties.provider_subscription_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["provider_subject_id", "provider_subscription_id", "status", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["provider_subject_id"]) -> MetaOapg.properties.provider_subject_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["provider_subscription_id"]) -> MetaOapg.properties.provider_subscription_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["provider_subject_id", "provider_subscription_id", "status", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        provider_subject_id: typing.Union[MetaOapg.properties.provider_subject_id, str, ],
        provider_subscription_id: typing.Union[MetaOapg.properties.provider_subscription_id, str, ],
        status: typing.Union[MetaOapg.properties.status, str, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'WatchlistSuppress':
        return super().__new__(
            cls,
            *_args,
            provider_subject_id=provider_subject_id,
            provider_subscription_id=provider_subscription_id,
            status=status,
            _configuration=_configuration,
            **kwargs,
        )
