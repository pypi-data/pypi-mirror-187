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


class ReversalModel(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "amount",
            "original_transaction_id",
        }
        
        class properties:
            amount = schemas.IntSchema
            original_transaction_id = schemas.UUIDSchema
            find_original_window_days = schemas.Int32Schema
            is_advice = schemas.BoolSchema
            
            
            class network_fees(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['NetworkFeeModel']:
                        return NetworkFeeModel
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['NetworkFeeModel'], typing.List['NetworkFeeModel']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'network_fees':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'NetworkFeeModel':
                    return super().__getitem__(i)
            __annotations__ = {
                "amount": amount,
                "original_transaction_id": original_transaction_id,
                "find_original_window_days": find_original_window_days,
                "is_advice": is_advice,
                "network_fees": network_fees,
            }
    
    amount: MetaOapg.properties.amount
    original_transaction_id: MetaOapg.properties.original_transaction_id
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["original_transaction_id"]) -> MetaOapg.properties.original_transaction_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["find_original_window_days"]) -> MetaOapg.properties.find_original_window_days: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_advice"]) -> MetaOapg.properties.is_advice: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["network_fees"]) -> MetaOapg.properties.network_fees: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["amount", "original_transaction_id", "find_original_window_days", "is_advice", "network_fees", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["original_transaction_id"]) -> MetaOapg.properties.original_transaction_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["find_original_window_days"]) -> typing.Union[MetaOapg.properties.find_original_window_days, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_advice"]) -> typing.Union[MetaOapg.properties.is_advice, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["network_fees"]) -> typing.Union[MetaOapg.properties.network_fees, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["amount", "original_transaction_id", "find_original_window_days", "is_advice", "network_fees", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        amount: typing.Union[MetaOapg.properties.amount, decimal.Decimal, int, ],
        original_transaction_id: typing.Union[MetaOapg.properties.original_transaction_id, str, uuid.UUID, ],
        find_original_window_days: typing.Union[MetaOapg.properties.find_original_window_days, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        is_advice: typing.Union[MetaOapg.properties.is_advice, bool, schemas.Unset] = schemas.unset,
        network_fees: typing.Union[MetaOapg.properties.network_fees, list, tuple, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ReversalModel':
        return super().__new__(
            cls,
            *_args,
            amount=amount,
            original_transaction_id=original_transaction_id,
            find_original_window_days=find_original_window_days,
            is_advice=is_advice,
            network_fees=network_fees,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.network_fee_model import NetworkFeeModel
