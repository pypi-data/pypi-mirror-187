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


class InternalAccount(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "currency",
            "status",
        }
        
        class properties:
            
            
            class currency(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    regex=[{
                        'pattern': r'^[A-Z]{3}$',  # noqa: E501
                    }]
            
            
            class status(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "ACTIVE": "ACTIVE",
                    }
                
                @schemas.classproperty
                def ACTIVE(cls):
                    return cls("ACTIVE")
            
            
            class account_number(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 17
                    min_length = 14
        
            @staticmethod
            def account_type() -> typing.Type['InternalAccountType']:
                return InternalAccountType
            
            
            class balances(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['Balance']:
                        return Balance
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['Balance'], typing.List['Balance']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'balances':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'Balance':
                    return super().__getitem__(i)
            
            
            class bank_routing(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 9
            creation_time = schemas.DateTimeSchema
            description = schemas.StrSchema
            
            
            class gl_type(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "ASSET": "ASSET",
                        "LIABILITY": "LIABILITY",
                        "EXPENSE": "EXPENSE",
                        "REVENUE": "REVENUE",
                    }
                
                @schemas.classproperty
                def ASSET(cls):
                    return cls("ASSET")
                
                @schemas.classproperty
                def LIABILITY(cls):
                    return cls("LIABILITY")
                
                @schemas.classproperty
                def EXPENSE(cls):
                    return cls("EXPENSE")
                
                @schemas.classproperty
                def REVENUE(cls):
                    return cls("REVENUE")
            id = schemas.UUIDSchema
            is_system_acc = schemas.BoolSchema
            last_updated_time = schemas.DateTimeSchema
        
            @staticmethod
            def purpose() -> typing.Type['InternalAccountPurpose']:
                return InternalAccountPurpose
            __annotations__ = {
                "currency": currency,
                "status": status,
                "account_number": account_number,
                "account_type": account_type,
                "balances": balances,
                "bank_routing": bank_routing,
                "creation_time": creation_time,
                "description": description,
                "gl_type": gl_type,
                "id": id,
                "is_system_acc": is_system_acc,
                "last_updated_time": last_updated_time,
                "purpose": purpose,
            }
    
    currency: MetaOapg.properties.currency
    status: MetaOapg.properties.status
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_number"]) -> MetaOapg.properties.account_number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_type"]) -> 'InternalAccountType': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["balances"]) -> MetaOapg.properties.balances: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bank_routing"]) -> MetaOapg.properties.bank_routing: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["gl_type"]) -> MetaOapg.properties.gl_type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_system_acc"]) -> MetaOapg.properties.is_system_acc: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["purpose"]) -> 'InternalAccountPurpose': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["currency", "status", "account_number", "account_type", "balances", "bank_routing", "creation_time", "description", "gl_type", "id", "is_system_acc", "last_updated_time", "purpose", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_number"]) -> typing.Union[MetaOapg.properties.account_number, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_type"]) -> typing.Union['InternalAccountType', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["balances"]) -> typing.Union[MetaOapg.properties.balances, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bank_routing"]) -> typing.Union[MetaOapg.properties.bank_routing, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["creation_time"]) -> typing.Union[MetaOapg.properties.creation_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["gl_type"]) -> typing.Union[MetaOapg.properties.gl_type, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_system_acc"]) -> typing.Union[MetaOapg.properties.is_system_acc, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_updated_time"]) -> typing.Union[MetaOapg.properties.last_updated_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["purpose"]) -> typing.Union['InternalAccountPurpose', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["currency", "status", "account_number", "account_type", "balances", "bank_routing", "creation_time", "description", "gl_type", "id", "is_system_acc", "last_updated_time", "purpose", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        currency: typing.Union[MetaOapg.properties.currency, str, ],
        status: typing.Union[MetaOapg.properties.status, str, ],
        account_number: typing.Union[MetaOapg.properties.account_number, str, schemas.Unset] = schemas.unset,
        account_type: typing.Union['InternalAccountType', schemas.Unset] = schemas.unset,
        balances: typing.Union[MetaOapg.properties.balances, list, tuple, schemas.Unset] = schemas.unset,
        bank_routing: typing.Union[MetaOapg.properties.bank_routing, str, schemas.Unset] = schemas.unset,
        creation_time: typing.Union[MetaOapg.properties.creation_time, str, datetime, schemas.Unset] = schemas.unset,
        description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
        gl_type: typing.Union[MetaOapg.properties.gl_type, str, schemas.Unset] = schemas.unset,
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        is_system_acc: typing.Union[MetaOapg.properties.is_system_acc, bool, schemas.Unset] = schemas.unset,
        last_updated_time: typing.Union[MetaOapg.properties.last_updated_time, str, datetime, schemas.Unset] = schemas.unset,
        purpose: typing.Union['InternalAccountPurpose', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'InternalAccount':
        return super().__new__(
            cls,
            *_args,
            currency=currency,
            status=status,
            account_number=account_number,
            account_type=account_type,
            balances=balances,
            bank_routing=bank_routing,
            creation_time=creation_time,
            description=description,
            gl_type=gl_type,
            id=id,
            is_system_acc=is_system_acc,
            last_updated_time=last_updated_time,
            purpose=purpose,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.balance import Balance
from synctera_client.model.internal_account_purpose import InternalAccountPurpose
from synctera_client.model.internal_account_type import InternalAccountType
