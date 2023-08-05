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


class ExternalAccountTransaction(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            amount = schemas.Int64Schema
            
            
            class authorized_date(
                schemas.DateBase,
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                class MetaOapg:
                    format = 'date'
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, date, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'authorized_date':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            
            
            class category(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.StrSchema
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'category':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            check_number = schemas.StrSchema
            currency = schemas.StrSchema
            date = schemas.DateSchema
            is_pending = schemas.BoolSchema
            merchant_name = schemas.StrSchema
            
            
            class payment_channel(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "IN_STORE": "IN_STORE",
                        "ONLINE": "ONLINE",
                        "OTHER": "OTHER",
                    }
                
                @schemas.classproperty
                def IN_STORE(cls):
                    return cls("IN_STORE")
                
                @schemas.classproperty
                def ONLINE(cls):
                    return cls("ONLINE")
                
                @schemas.classproperty
                def OTHER(cls):
                    return cls("OTHER")
            payment_method = schemas.StrSchema
            transaction_id = schemas.StrSchema
            __annotations__ = {
                "amount": amount,
                "authorized_date": authorized_date,
                "category": category,
                "check_number": check_number,
                "currency": currency,
                "date": date,
                "is_pending": is_pending,
                "merchant_name": merchant_name,
                "payment_channel": payment_channel,
                "payment_method": payment_method,
                "transaction_id": transaction_id,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["authorized_date"]) -> MetaOapg.properties.authorized_date: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["category"]) -> MetaOapg.properties.category: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["check_number"]) -> MetaOapg.properties.check_number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["date"]) -> MetaOapg.properties.date: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_pending"]) -> MetaOapg.properties.is_pending: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["merchant_name"]) -> MetaOapg.properties.merchant_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["payment_channel"]) -> MetaOapg.properties.payment_channel: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["payment_method"]) -> MetaOapg.properties.payment_method: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["transaction_id"]) -> MetaOapg.properties.transaction_id: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["amount", "authorized_date", "category", "check_number", "currency", "date", "is_pending", "merchant_name", "payment_channel", "payment_method", "transaction_id", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["amount"]) -> typing.Union[MetaOapg.properties.amount, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["authorized_date"]) -> typing.Union[MetaOapg.properties.authorized_date, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["category"]) -> typing.Union[MetaOapg.properties.category, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["check_number"]) -> typing.Union[MetaOapg.properties.check_number, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["currency"]) -> typing.Union[MetaOapg.properties.currency, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["date"]) -> typing.Union[MetaOapg.properties.date, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_pending"]) -> typing.Union[MetaOapg.properties.is_pending, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["merchant_name"]) -> typing.Union[MetaOapg.properties.merchant_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["payment_channel"]) -> typing.Union[MetaOapg.properties.payment_channel, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["payment_method"]) -> typing.Union[MetaOapg.properties.payment_method, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["transaction_id"]) -> typing.Union[MetaOapg.properties.transaction_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["amount", "authorized_date", "category", "check_number", "currency", "date", "is_pending", "merchant_name", "payment_channel", "payment_method", "transaction_id", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        amount: typing.Union[MetaOapg.properties.amount, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        authorized_date: typing.Union[MetaOapg.properties.authorized_date, None, str, date, schemas.Unset] = schemas.unset,
        category: typing.Union[MetaOapg.properties.category, list, tuple, schemas.Unset] = schemas.unset,
        check_number: typing.Union[MetaOapg.properties.check_number, str, schemas.Unset] = schemas.unset,
        currency: typing.Union[MetaOapg.properties.currency, str, schemas.Unset] = schemas.unset,
        date: typing.Union[MetaOapg.properties.date, str, date, schemas.Unset] = schemas.unset,
        is_pending: typing.Union[MetaOapg.properties.is_pending, bool, schemas.Unset] = schemas.unset,
        merchant_name: typing.Union[MetaOapg.properties.merchant_name, str, schemas.Unset] = schemas.unset,
        payment_channel: typing.Union[MetaOapg.properties.payment_channel, str, schemas.Unset] = schemas.unset,
        payment_method: typing.Union[MetaOapg.properties.payment_method, str, schemas.Unset] = schemas.unset,
        transaction_id: typing.Union[MetaOapg.properties.transaction_id, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ExternalAccountTransaction':
        return super().__new__(
            cls,
            *_args,
            amount=amount,
            authorized_date=authorized_date,
            category=category,
            check_number=check_number,
            currency=currency,
            date=date,
            is_pending=is_pending,
            merchant_name=merchant_name,
            payment_channel=payment_channel,
            payment_method=payment_method,
            transaction_id=transaction_id,
            _configuration=_configuration,
            **kwargs,
        )
