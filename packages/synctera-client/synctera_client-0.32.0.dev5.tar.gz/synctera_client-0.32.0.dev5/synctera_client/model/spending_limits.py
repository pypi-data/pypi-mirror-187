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


class SpendingLimits(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Account spending limits
    """


    class MetaOapg:
        
        class properties:
        
            @staticmethod
            def day() -> typing.Type['SpendingLimitWithTime']:
                return SpendingLimitWithTime
            description = schemas.StrSchema
        
            @staticmethod
            def lifetime() -> typing.Type['SpendingLimitWithTime']:
                return SpendingLimitWithTime
        
            @staticmethod
            def month() -> typing.Type['SpendingLimitWithTime']:
                return SpendingLimitWithTime
            
            
            class transaction(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        
                        
                        class amount(
                            schemas.Int64Schema
                        ):
                        
                        
                            class MetaOapg:
                                format = 'int64'
                                inclusive_minimum = 0
                        __annotations__ = {
                            "amount": amount,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["amount", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["amount"]) -> typing.Union[MetaOapg.properties.amount, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["amount", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    amount: typing.Union[MetaOapg.properties.amount, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'transaction':
                    return super().__new__(
                        cls,
                        *_args,
                        amount=amount,
                        _configuration=_configuration,
                        **kwargs,
                    )
        
            @staticmethod
            def week() -> typing.Type['SpendingLimitWithTime']:
                return SpendingLimitWithTime
            __annotations__ = {
                "day": day,
                "description": description,
                "lifetime": lifetime,
                "month": month,
                "transaction": transaction,
                "week": week,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["day"]) -> 'SpendingLimitWithTime': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["lifetime"]) -> 'SpendingLimitWithTime': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["month"]) -> 'SpendingLimitWithTime': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["transaction"]) -> MetaOapg.properties.transaction: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["week"]) -> 'SpendingLimitWithTime': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["day", "description", "lifetime", "month", "transaction", "week", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["day"]) -> typing.Union['SpendingLimitWithTime', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["lifetime"]) -> typing.Union['SpendingLimitWithTime', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["month"]) -> typing.Union['SpendingLimitWithTime', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["transaction"]) -> typing.Union[MetaOapg.properties.transaction, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["week"]) -> typing.Union['SpendingLimitWithTime', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["day", "description", "lifetime", "month", "transaction", "week", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        day: typing.Union['SpendingLimitWithTime', schemas.Unset] = schemas.unset,
        description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
        lifetime: typing.Union['SpendingLimitWithTime', schemas.Unset] = schemas.unset,
        month: typing.Union['SpendingLimitWithTime', schemas.Unset] = schemas.unset,
        transaction: typing.Union[MetaOapg.properties.transaction, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        week: typing.Union['SpendingLimitWithTime', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'SpendingLimits':
        return super().__new__(
            cls,
            *_args,
            day=day,
            description=description,
            lifetime=lifetime,
            month=month,
            transaction=transaction,
            week=week,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.spending_limit_with_time import SpendingLimitWithTime
