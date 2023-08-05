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


class SpendControlUpdateRequest(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            action_case = schemas.BoolSchema
            action_decline = schemas.BoolSchema
            
            
            class amount_limit(
                schemas.Int64Schema
            ):
                pass
        
            @staticmethod
            def direction() -> typing.Type['SpendControlDirection']:
                return SpendControlDirection
            is_active = schemas.BoolSchema
            name = schemas.StrSchema
        
            @staticmethod
            def payment_types() -> typing.Type['PaymentTypeList']:
                return PaymentTypeList
        
            @staticmethod
            def time_range() -> typing.Type['SpendControlTimeRange']:
                return SpendControlTimeRange
            __annotations__ = {
                "action_case": action_case,
                "action_decline": action_decline,
                "amount_limit": amount_limit,
                "direction": direction,
                "is_active": is_active,
                "name": name,
                "payment_types": payment_types,
                "time_range": time_range,
            }
        additional_properties = schemas.NotAnyTypeSchema
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["action_case"]) -> MetaOapg.properties.action_case: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["action_decline"]) -> MetaOapg.properties.action_decline: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["amount_limit"]) -> MetaOapg.properties.amount_limit: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["direction"]) -> 'SpendControlDirection': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_active"]) -> MetaOapg.properties.is_active: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["payment_types"]) -> 'PaymentTypeList': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["time_range"]) -> 'SpendControlTimeRange': ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["action_case"], typing_extensions.Literal["action_decline"], typing_extensions.Literal["amount_limit"], typing_extensions.Literal["direction"], typing_extensions.Literal["is_active"], typing_extensions.Literal["name"], typing_extensions.Literal["payment_types"], typing_extensions.Literal["time_range"], ]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["action_case"]) -> typing.Union[MetaOapg.properties.action_case, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["action_decline"]) -> typing.Union[MetaOapg.properties.action_decline, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["amount_limit"]) -> typing.Union[MetaOapg.properties.amount_limit, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["direction"]) -> typing.Union['SpendControlDirection', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_active"]) -> typing.Union[MetaOapg.properties.is_active, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["payment_types"]) -> typing.Union['PaymentTypeList', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["time_range"]) -> typing.Union['SpendControlTimeRange', schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["action_case"], typing_extensions.Literal["action_decline"], typing_extensions.Literal["amount_limit"], typing_extensions.Literal["direction"], typing_extensions.Literal["is_active"], typing_extensions.Literal["name"], typing_extensions.Literal["payment_types"], typing_extensions.Literal["time_range"], ]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        action_case: typing.Union[MetaOapg.properties.action_case, bool, schemas.Unset] = schemas.unset,
        action_decline: typing.Union[MetaOapg.properties.action_decline, bool, schemas.Unset] = schemas.unset,
        amount_limit: typing.Union[MetaOapg.properties.amount_limit, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        direction: typing.Union['SpendControlDirection', schemas.Unset] = schemas.unset,
        is_active: typing.Union[MetaOapg.properties.is_active, bool, schemas.Unset] = schemas.unset,
        name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
        payment_types: typing.Union['PaymentTypeList', schemas.Unset] = schemas.unset,
        time_range: typing.Union['SpendControlTimeRange', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'SpendControlUpdateRequest':
        return super().__new__(
            cls,
            *_args,
            action_case=action_case,
            action_decline=action_decline,
            amount_limit=amount_limit,
            direction=direction,
            is_active=is_active,
            name=name,
            payment_types=payment_types,
            time_range=time_range,
            _configuration=_configuration,
        )

from synctera_client.model.payment_type_list import PaymentTypeList
from synctera_client.model.spend_control_direction import SpendControlDirection
from synctera_client.model.spend_control_time_range import SpendControlTimeRange
