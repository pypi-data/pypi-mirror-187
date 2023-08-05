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


class CardAcceptorModel(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            
            
            class address(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 255
                    min_length = 0
            
            
            class city(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 40
                    min_length = 0
            country = schemas.StrSchema
            ecommerce_security_level_indicator = schemas.StrSchema
            
            
            class mcc(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 5
                    min_length = 0
            
            
            class name(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 50
                    min_length = 0
            partial_approval_capable = schemas.BoolSchema
            state = schemas.StrSchema
            
            
            class zip(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 10
                    min_length = 0
            __annotations__ = {
                "address": address,
                "city": city,
                "country": country,
                "ecommerce_security_level_indicator": ecommerce_security_level_indicator,
                "mcc": mcc,
                "name": name,
                "partial_approval_capable": partial_approval_capable,
                "state": state,
                "zip": zip,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["address"]) -> MetaOapg.properties.address: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["city"]) -> MetaOapg.properties.city: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["country"]) -> MetaOapg.properties.country: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["ecommerce_security_level_indicator"]) -> MetaOapg.properties.ecommerce_security_level_indicator: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["mcc"]) -> MetaOapg.properties.mcc: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["partial_approval_capable"]) -> MetaOapg.properties.partial_approval_capable: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["state"]) -> MetaOapg.properties.state: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["zip"]) -> MetaOapg.properties.zip: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["address", "city", "country", "ecommerce_security_level_indicator", "mcc", "name", "partial_approval_capable", "state", "zip", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["address"]) -> typing.Union[MetaOapg.properties.address, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["city"]) -> typing.Union[MetaOapg.properties.city, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["country"]) -> typing.Union[MetaOapg.properties.country, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["ecommerce_security_level_indicator"]) -> typing.Union[MetaOapg.properties.ecommerce_security_level_indicator, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["mcc"]) -> typing.Union[MetaOapg.properties.mcc, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["partial_approval_capable"]) -> typing.Union[MetaOapg.properties.partial_approval_capable, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["state"]) -> typing.Union[MetaOapg.properties.state, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["zip"]) -> typing.Union[MetaOapg.properties.zip, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["address", "city", "country", "ecommerce_security_level_indicator", "mcc", "name", "partial_approval_capable", "state", "zip", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        address: typing.Union[MetaOapg.properties.address, str, schemas.Unset] = schemas.unset,
        city: typing.Union[MetaOapg.properties.city, str, schemas.Unset] = schemas.unset,
        country: typing.Union[MetaOapg.properties.country, str, schemas.Unset] = schemas.unset,
        ecommerce_security_level_indicator: typing.Union[MetaOapg.properties.ecommerce_security_level_indicator, str, schemas.Unset] = schemas.unset,
        mcc: typing.Union[MetaOapg.properties.mcc, str, schemas.Unset] = schemas.unset,
        name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
        partial_approval_capable: typing.Union[MetaOapg.properties.partial_approval_capable, bool, schemas.Unset] = schemas.unset,
        state: typing.Union[MetaOapg.properties.state, str, schemas.Unset] = schemas.unset,
        zip: typing.Union[MetaOapg.properties.zip, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CardAcceptorModel':
        return super().__new__(
            cls,
            *_args,
            address=address,
            city=city,
            country=country,
            ecommerce_security_level_indicator=ecommerce_security_level_indicator,
            mcc=mcc,
            name=name,
            partial_approval_capable=partial_approval_capable,
            state=state,
            zip=zip,
            _configuration=_configuration,
            **kwargs,
        )
