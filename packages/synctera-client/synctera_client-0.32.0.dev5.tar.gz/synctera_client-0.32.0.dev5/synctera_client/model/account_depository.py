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


class AccountDepository(
    schemas.ComposedBase,
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Account representing either a checking or saving account.
    """


    class MetaOapg:
        
        
        class all_of_1(
            schemas.AnyTypeSchema,
        ):
        
        
            class MetaOapg:
                
                class properties:
                
                    @staticmethod
                    def balance_ceiling() -> typing.Type['BalanceCeiling']:
                        return BalanceCeiling
                
                    @staticmethod
                    def balance_floor() -> typing.Type['BalanceFloor']:
                        return BalanceFloor
                    
                    
                    class fee_product_ids(
                        schemas.ListSchema
                    ):
                    
                    
                        class MetaOapg:
                            items = schemas.UUIDSchema
                    
                        def __new__(
                            cls,
                            _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, uuid.UUID, ]], typing.List[typing.Union[MetaOapg.items, str, uuid.UUID, ]]],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                        ) -> 'fee_product_ids':
                            return super().__new__(
                                cls,
                                _arg,
                                _configuration=_configuration,
                            )
                    
                        def __getitem__(self, i: int) -> MetaOapg.items:
                            return super().__getitem__(i)
                    interest_product_id = schemas.UUIDSchema
                    
                    
                    class overdraft_limit(
                        schemas.Int64Schema
                    ):
                    
                    
                        class MetaOapg:
                            format = 'int64'
                            inclusive_minimum = 0
                
                    @staticmethod
                    def spend_control_ids() -> typing.Type['SpendControlIds']:
                        return SpendControlIds
                
                    @staticmethod
                    def spending_limits() -> typing.Type['SpendingLimits']:
                        return SpendingLimits
                    __annotations__ = {
                        "balance_ceiling": balance_ceiling,
                        "balance_floor": balance_floor,
                        "fee_product_ids": fee_product_ids,
                        "interest_product_id": interest_product_id,
                        "overdraft_limit": overdraft_limit,
                        "spend_control_ids": spend_control_ids,
                        "spending_limits": spending_limits,
                    }
        
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["balance_ceiling"]) -> 'BalanceCeiling': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["balance_floor"]) -> 'BalanceFloor': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["fee_product_ids"]) -> MetaOapg.properties.fee_product_ids: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["interest_product_id"]) -> MetaOapg.properties.interest_product_id: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["overdraft_limit"]) -> MetaOapg.properties.overdraft_limit: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["spend_control_ids"]) -> 'SpendControlIds': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["spending_limits"]) -> 'SpendingLimits': ...
            
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            
            def __getitem__(self, name: typing.Union[typing_extensions.Literal["balance_ceiling", "balance_floor", "fee_product_ids", "interest_product_id", "overdraft_limit", "spend_control_ids", "spending_limits", ], str]):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["balance_ceiling"]) -> typing.Union['BalanceCeiling', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["balance_floor"]) -> typing.Union['BalanceFloor', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["fee_product_ids"]) -> typing.Union[MetaOapg.properties.fee_product_ids, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["interest_product_id"]) -> typing.Union[MetaOapg.properties.interest_product_id, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["overdraft_limit"]) -> typing.Union[MetaOapg.properties.overdraft_limit, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["spend_control_ids"]) -> typing.Union['SpendControlIds', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["spending_limits"]) -> typing.Union['SpendingLimits', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            
            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["balance_ceiling", "balance_floor", "fee_product_ids", "interest_product_id", "overdraft_limit", "spend_control_ids", "spending_limits", ], str]):
                return super().get_item_oapg(name)
            
        
            def __new__(
                cls,
                *_args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                balance_ceiling: typing.Union['BalanceCeiling', schemas.Unset] = schemas.unset,
                balance_floor: typing.Union['BalanceFloor', schemas.Unset] = schemas.unset,
                fee_product_ids: typing.Union[MetaOapg.properties.fee_product_ids, list, tuple, schemas.Unset] = schemas.unset,
                interest_product_id: typing.Union[MetaOapg.properties.interest_product_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
                overdraft_limit: typing.Union[MetaOapg.properties.overdraft_limit, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                spend_control_ids: typing.Union['SpendControlIds', schemas.Unset] = schemas.unset,
                spending_limits: typing.Union['SpendingLimits', schemas.Unset] = schemas.unset,
                _configuration: typing.Optional[schemas.Configuration] = None,
                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
            ) -> 'all_of_1':
                return super().__new__(
                    cls,
                    *_args,
                    balance_ceiling=balance_ceiling,
                    balance_floor=balance_floor,
                    fee_product_ids=fee_product_ids,
                    interest_product_id=interest_product_id,
                    overdraft_limit=overdraft_limit,
                    spend_control_ids=spend_control_ids,
                    spending_limits=spending_limits,
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
    ) -> 'AccountDepository':
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.account_base import AccountBase
from synctera_client.model.balance_ceiling import BalanceCeiling
from synctera_client.model.balance_floor import BalanceFloor
from synctera_client.model.spend_control_ids import SpendControlIds
from synctera_client.model.spending_limits import SpendingLimits
