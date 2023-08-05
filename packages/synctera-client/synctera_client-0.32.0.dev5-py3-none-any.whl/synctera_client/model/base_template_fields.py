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


class BaseTemplateFields(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "account_type",
            "bank_country",
            "currency",
        }
        
        class properties:
        
            @staticmethod
            def account_type() -> typing.Type['AccountType']:
                return AccountType
            
            
            class bank_country(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    regex=[{
                        'pattern': r'^[A-Z]{2,3}$',  # noqa: E501
                    }]
            
            
            class currency(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    regex=[{
                        'pattern': r'^[A-Z]{3}$',  # noqa: E501
                    }]
            __annotations__ = {
                "account_type": account_type,
                "bank_country": bank_country,
                "currency": currency,
            }
    
    account_type: 'AccountType'
    bank_country: MetaOapg.properties.bank_country
    currency: MetaOapg.properties.currency
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_type"]) -> 'AccountType': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bank_country"]) -> MetaOapg.properties.bank_country: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["account_type", "bank_country", "currency", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_type"]) -> 'AccountType': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bank_country"]) -> MetaOapg.properties.bank_country: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["account_type", "bank_country", "currency", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        account_type: 'AccountType',
        bank_country: typing.Union[MetaOapg.properties.bank_country, str, ],
        currency: typing.Union[MetaOapg.properties.currency, str, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'BaseTemplateFields':
        return super().__new__(
            cls,
            *_args,
            account_type=account_type,
            bank_country=bank_country,
            currency=currency,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.account_type import AccountType
