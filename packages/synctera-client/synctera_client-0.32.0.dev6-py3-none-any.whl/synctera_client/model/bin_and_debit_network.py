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


class BinAndDebitNetwork(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "bin",
            "debit_network",
            "bank_network_id",
        }
        
        class properties:
            bank_network_id = schemas.StrSchema
        
            @staticmethod
            def bin() -> typing.Type['Bin']:
                return Bin
        
            @staticmethod
            def debit_network() -> typing.Type['DebitNetwork']:
                return DebitNetwork
            __annotations__ = {
                "bank_network_id": bank_network_id,
                "bin": bin,
                "debit_network": debit_network,
            }
    
    bin: 'Bin'
    debit_network: 'DebitNetwork'
    bank_network_id: MetaOapg.properties.bank_network_id
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bank_network_id"]) -> MetaOapg.properties.bank_network_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bin"]) -> 'Bin': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["debit_network"]) -> 'DebitNetwork': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["bank_network_id", "bin", "debit_network", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bank_network_id"]) -> MetaOapg.properties.bank_network_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bin"]) -> 'Bin': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["debit_network"]) -> 'DebitNetwork': ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["bank_network_id", "bin", "debit_network", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        bin: 'Bin',
        debit_network: 'DebitNetwork',
        bank_network_id: typing.Union[MetaOapg.properties.bank_network_id, str, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'BinAndDebitNetwork':
        return super().__new__(
            cls,
            *_args,
            bin=bin,
            debit_network=debit_network,
            bank_network_id=bank_network_id,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.bin import Bin
from synctera_client.model.debit_network import DebitNetwork
