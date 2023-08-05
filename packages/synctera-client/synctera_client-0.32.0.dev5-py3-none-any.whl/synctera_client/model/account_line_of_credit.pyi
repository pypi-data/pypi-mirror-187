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


class AccountLineOfCredit(
    schemas.ComposedBase,
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Account representing a line of credit account.
    """


    class MetaOapg:
        
        
        class all_of_1(
            schemas.DictSchema
        ):
        
        
            class MetaOapg:
                
                class properties:
                    
                    
                    class chargeoff_period(
                        schemas.IntSchema
                    ):
                        pass
                    
                    
                    class credit_limit(
                        schemas.Int64Schema
                    ):
                        pass
                    
                    
                    class delinquency_period(
                        schemas.IntSchema
                    ):
                        pass
                    
                    
                    class grace_period(
                        schemas.IntSchema
                    ):
                        pass
                    interest_product_id = schemas.UUIDSchema
                
                    @staticmethod
                    def minimum_payment() -> typing.Type['MinimumPaymentPartial']:
                        return MinimumPaymentPartial
                    __annotations__ = {
                        "chargeoff_period": chargeoff_period,
                        "credit_limit": credit_limit,
                        "delinquency_period": delinquency_period,
                        "grace_period": grace_period,
                        "interest_product_id": interest_product_id,
                        "minimum_payment": minimum_payment,
                    }
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["chargeoff_period"]) -> MetaOapg.properties.chargeoff_period: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["credit_limit"]) -> MetaOapg.properties.credit_limit: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["delinquency_period"]) -> MetaOapg.properties.delinquency_period: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["grace_period"]) -> MetaOapg.properties.grace_period: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["interest_product_id"]) -> MetaOapg.properties.interest_product_id: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["minimum_payment"]) -> 'MinimumPaymentPartial': ...
            
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            
            def __getitem__(self, name: typing.Union[typing_extensions.Literal["chargeoff_period", "credit_limit", "delinquency_period", "grace_period", "interest_product_id", "minimum_payment", ], str]):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["chargeoff_period"]) -> typing.Union[MetaOapg.properties.chargeoff_period, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["credit_limit"]) -> typing.Union[MetaOapg.properties.credit_limit, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["delinquency_period"]) -> typing.Union[MetaOapg.properties.delinquency_period, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["grace_period"]) -> typing.Union[MetaOapg.properties.grace_period, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["interest_product_id"]) -> typing.Union[MetaOapg.properties.interest_product_id, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["minimum_payment"]) -> typing.Union['MinimumPaymentPartial', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            
            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["chargeoff_period", "credit_limit", "delinquency_period", "grace_period", "interest_product_id", "minimum_payment", ], str]):
                return super().get_item_oapg(name)
            
        
            def __new__(
                cls,
                *_args: typing.Union[dict, frozendict.frozendict, ],
                chargeoff_period: typing.Union[MetaOapg.properties.chargeoff_period, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                credit_limit: typing.Union[MetaOapg.properties.credit_limit, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                delinquency_period: typing.Union[MetaOapg.properties.delinquency_period, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                grace_period: typing.Union[MetaOapg.properties.grace_period, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                interest_product_id: typing.Union[MetaOapg.properties.interest_product_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
                minimum_payment: typing.Union['MinimumPaymentPartial', schemas.Unset] = schemas.unset,
                _configuration: typing.Optional[schemas.Configuration] = None,
                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
            ) -> 'all_of_1':
                return super().__new__(
                    cls,
                    *_args,
                    chargeoff_period=chargeoff_period,
                    credit_limit=credit_limit,
                    delinquency_period=delinquency_period,
                    grace_period=grace_period,
                    interest_product_id=interest_product_id,
                    minimum_payment=minimum_payment,
                    _configuration=_configuration,
                    **kwargs,
                )
        
        @classmethod
        @functools.lru_cache()
        def all_of(cls):
            # we need this here to make our import statements work
            # we must store _composed_schemas in here so the code is only run
            # when we invoke this method. If we kept this at the class
            # level we would get an error because the class level
            # code would be run when this module is imported, and these composed
            # classes don't exist yet because their module has not finished
            # loading
            return [
                AccountBase,
                cls.all_of_1,
            ]


    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'AccountLineOfCredit':
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.account_base import AccountBase
from synctera_client.model.minimum_payment_partial import MinimumPaymentPartial
