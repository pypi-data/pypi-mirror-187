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


class NetworkFeeModel(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "amount",
            "type",
        }
        
        class properties:
            amount = schemas.IntSchema
            
            
            class type(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def ISSUER_FEE(cls):
                    return cls("ISSUER_FEE")
                
                @schemas.classproperty
                def SWITCH_FEE(cls):
                    return cls("SWITCH_FEE")
                
                @schemas.classproperty
                def PINDEBIT_ASSOC_FEE(cls):
                    return cls("PINDEBIT_ASSOC_FEE")
                
                @schemas.classproperty
                def ACQUIRER_FEE(cls):
                    return cls("ACQUIRER_FEE")
                
                @schemas.classproperty
                def INTERCHANGE_FEE(cls):
                    return cls("INTERCHANGE_FEE")
                
                @schemas.classproperty
                def CUR_CONV_CARDHOLDER_FEE(cls):
                    return cls("CUR_CONV_CARDHOLDER_FEE")
                
                @schemas.classproperty
                def CUR_CONV_ISSUER_FEE(cls):
                    return cls("CUR_CONV_ISSUER_FEE")
                
                @schemas.classproperty
                def CROSS_BORDER_ISSUER_FEE(cls):
                    return cls("CROSS_BORDER_ISSUER_FEE")
            
            
            class credit_debit(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def C(cls):
                    return cls("C")
                
                @schemas.classproperty
                def D(cls):
                    return cls("D")
            __annotations__ = {
                "amount": amount,
                "type": type,
                "credit_debit": credit_debit,
            }
    
    amount: MetaOapg.properties.amount
    type: MetaOapg.properties.type
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["credit_debit"]) -> MetaOapg.properties.credit_debit: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["amount", "type", "credit_debit", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["credit_debit"]) -> typing.Union[MetaOapg.properties.credit_debit, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["amount", "type", "credit_debit", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        amount: typing.Union[MetaOapg.properties.amount, decimal.Decimal, int, ],
        type: typing.Union[MetaOapg.properties.type, str, ],
        credit_debit: typing.Union[MetaOapg.properties.credit_debit, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'NetworkFeeModel':
        return super().__new__(
            cls,
            *_args,
            amount=amount,
            type=type,
            credit_debit=credit_debit,
            _configuration=_configuration,
            **kwargs,
        )
