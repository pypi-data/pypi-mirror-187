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


class ExternalCardVerifications(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Verify card passed AVS and CVV checks and if it able to perform PUSH/PULL transfers.
    """


    class MetaOapg:
        required = {
            "pull_enabled",
            "cvv2_result",
            "push_enabled",
            "address_verification_result",
            "state",
        }
        
        class properties:
            
            
            class address_verification_result(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def VERIFIED(cls):
                    return cls("VERIFIED")
                
                @schemas.classproperty
                def NOT_VERIFIED(cls):
                    return cls("NOT_VERIFIED")
                
                @schemas.classproperty
                def ADDRESS_MISMATCH(cls):
                    return cls("ADDRESS_MISMATCH")
                
                @schemas.classproperty
                def ZIP_MISMATCH(cls):
                    return cls("ZIP_MISMATCH")
                
                @schemas.classproperty
                def ADDRESS_AND_ZIP_MISMATCH(cls):
                    return cls("ADDRESS_AND_ZIP_MISMATCH")
            
            
            class cvv2_result(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def VERIFIED(cls):
                    return cls("VERIFIED")
                
                @schemas.classproperty
                def NOT_VERIFIED(cls):
                    return cls("NOT_VERIFIED")
                
                @schemas.classproperty
                def CVV_MISMATCH(cls):
                    return cls("CVV_MISMATCH")
                
                @schemas.classproperty
                def NOT_SUPPORTED(cls):
                    return cls("NOT_SUPPORTED")
            pull_enabled = schemas.BoolSchema
            push_enabled = schemas.BoolSchema
            
            
            class state(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def SUCCEEDED(cls):
                    return cls("SUCCEEDED")
                
                @schemas.classproperty
                def FAILED(cls):
                    return cls("FAILED")
            __annotations__ = {
                "address_verification_result": address_verification_result,
                "cvv2_result": cvv2_result,
                "pull_enabled": pull_enabled,
                "push_enabled": push_enabled,
                "state": state,
            }
    
    pull_enabled: MetaOapg.properties.pull_enabled
    cvv2_result: MetaOapg.properties.cvv2_result
    push_enabled: MetaOapg.properties.push_enabled
    address_verification_result: MetaOapg.properties.address_verification_result
    state: MetaOapg.properties.state
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["address_verification_result"]) -> MetaOapg.properties.address_verification_result: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["cvv2_result"]) -> MetaOapg.properties.cvv2_result: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pull_enabled"]) -> MetaOapg.properties.pull_enabled: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["push_enabled"]) -> MetaOapg.properties.push_enabled: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["state"]) -> MetaOapg.properties.state: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["address_verification_result", "cvv2_result", "pull_enabled", "push_enabled", "state", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["address_verification_result"]) -> MetaOapg.properties.address_verification_result: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["cvv2_result"]) -> MetaOapg.properties.cvv2_result: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pull_enabled"]) -> MetaOapg.properties.pull_enabled: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["push_enabled"]) -> MetaOapg.properties.push_enabled: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["state"]) -> MetaOapg.properties.state: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["address_verification_result", "cvv2_result", "pull_enabled", "push_enabled", "state", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        pull_enabled: typing.Union[MetaOapg.properties.pull_enabled, bool, ],
        cvv2_result: typing.Union[MetaOapg.properties.cvv2_result, str, ],
        push_enabled: typing.Union[MetaOapg.properties.push_enabled, bool, ],
        address_verification_result: typing.Union[MetaOapg.properties.address_verification_result, str, ],
        state: typing.Union[MetaOapg.properties.state, str, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ExternalCardVerifications':
        return super().__new__(
            cls,
            *_args,
            pull_enabled=pull_enabled,
            cvv2_result=cvv2_result,
            push_enabled=push_enabled,
            address_verification_result=address_verification_result,
            state=state,
            _configuration=_configuration,
            **kwargs,
        )
