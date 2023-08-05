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


class FinancialRequestModel(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "amount",
            "mid",
            "card_acceptor",
            "card_id",
        }
        
        class properties:
            amount = schemas.IntSchema
        
            @staticmethod
            def card_acceptor() -> typing.Type['CardAcceptorModel']:
                return CardAcceptorModel
            card_id = schemas.UUIDSchema
            
            
            class mid(
                schemas.StrSchema
            ):
                pass
            cash_back_amount = schemas.IntSchema
            is_pre_auth = schemas.BoolSchema
            
            
            class pin(
                schemas.StrSchema
            ):
                pass
        
            @staticmethod
            def transaction_options() -> typing.Type['TransactionOptions']:
                return TransactionOptions
            __annotations__ = {
                "amount": amount,
                "card_acceptor": card_acceptor,
                "card_id": card_id,
                "mid": mid,
                "cash_back_amount": cash_back_amount,
                "is_pre_auth": is_pre_auth,
                "pin": pin,
                "transaction_options": transaction_options,
            }
    
    amount: MetaOapg.properties.amount
    mid: MetaOapg.properties.mid
    card_acceptor: 'CardAcceptorModel'
    card_id: MetaOapg.properties.card_id
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["card_acceptor"]) -> 'CardAcceptorModel': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["card_id"]) -> MetaOapg.properties.card_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["mid"]) -> MetaOapg.properties.mid: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["cash_back_amount"]) -> MetaOapg.properties.cash_back_amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_pre_auth"]) -> MetaOapg.properties.is_pre_auth: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pin"]) -> MetaOapg.properties.pin: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["transaction_options"]) -> 'TransactionOptions': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["amount", "card_acceptor", "card_id", "mid", "cash_back_amount", "is_pre_auth", "pin", "transaction_options", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["card_acceptor"]) -> 'CardAcceptorModel': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["card_id"]) -> MetaOapg.properties.card_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["mid"]) -> MetaOapg.properties.mid: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["cash_back_amount"]) -> typing.Union[MetaOapg.properties.cash_back_amount, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_pre_auth"]) -> typing.Union[MetaOapg.properties.is_pre_auth, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pin"]) -> typing.Union[MetaOapg.properties.pin, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["transaction_options"]) -> typing.Union['TransactionOptions', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["amount", "card_acceptor", "card_id", "mid", "cash_back_amount", "is_pre_auth", "pin", "transaction_options", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        amount: typing.Union[MetaOapg.properties.amount, decimal.Decimal, int, ],
        mid: typing.Union[MetaOapg.properties.mid, str, ],
        card_acceptor: 'CardAcceptorModel',
        card_id: typing.Union[MetaOapg.properties.card_id, str, uuid.UUID, ],
        cash_back_amount: typing.Union[MetaOapg.properties.cash_back_amount, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        is_pre_auth: typing.Union[MetaOapg.properties.is_pre_auth, bool, schemas.Unset] = schemas.unset,
        pin: typing.Union[MetaOapg.properties.pin, str, schemas.Unset] = schemas.unset,
        transaction_options: typing.Union['TransactionOptions', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'FinancialRequestModel':
        return super().__new__(
            cls,
            *_args,
            amount=amount,
            mid=mid,
            card_acceptor=card_acceptor,
            card_id=card_id,
            cash_back_amount=cash_back_amount,
            is_pre_auth=is_pre_auth,
            pin=pin,
            transaction_options=transaction_options,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.card_acceptor_model import CardAcceptorModel
from synctera_client.model.transaction_options import TransactionOptions
