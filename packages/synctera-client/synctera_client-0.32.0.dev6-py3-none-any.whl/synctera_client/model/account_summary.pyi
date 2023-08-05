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


class AccountSummary(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
            account_number = schemas.StrSchema
            account_status = schemas.StrSchema
            account_type = schemas.StrSchema
            
            
            class balance_ceiling(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        balance = schemas.Int64Schema
                        __annotations__ = {
                            "balance": balance,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["balance"]) -> MetaOapg.properties.balance: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["balance", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["balance"]) -> typing.Union[MetaOapg.properties.balance, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["balance", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    balance: typing.Union[MetaOapg.properties.balance, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'balance_ceiling':
                    return super().__new__(
                        cls,
                        *_args,
                        balance=balance,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class balance_floor(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        balance = schemas.Int64Schema
                        __annotations__ = {
                            "balance": balance,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["balance"]) -> MetaOapg.properties.balance: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["balance", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["balance"]) -> typing.Union[MetaOapg.properties.balance, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["balance", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    balance: typing.Union[MetaOapg.properties.balance, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'balance_floor':
                    return super().__new__(
                        cls,
                        *_args,
                        balance=balance,
                        _configuration=_configuration,
                        **kwargs,
                    )
            creation_time = schemas.DateTimeSchema
            
            
            class currency(
                schemas.StrSchema
            ):
                pass
            customer_type = schemas.StrSchema
        
            @staticmethod
            def financial_institution() -> typing.Type['FinancialInstitution']:
                return FinancialInstitution
            id = schemas.UUIDSchema
            last_updated_time = schemas.DateTimeSchema
            nickname = schemas.StrSchema
            __annotations__ = {
                "account_number": account_number,
                "account_status": account_status,
                "account_type": account_type,
                "balance_ceiling": balance_ceiling,
                "balance_floor": balance_floor,
                "creation_time": creation_time,
                "currency": currency,
                "customer_type": customer_type,
                "financial_institution": financial_institution,
                "id": id,
                "last_updated_time": last_updated_time,
                "nickname": nickname,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_number"]) -> MetaOapg.properties.account_number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_status"]) -> MetaOapg.properties.account_status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_type"]) -> MetaOapg.properties.account_type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["balance_ceiling"]) -> MetaOapg.properties.balance_ceiling: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["balance_floor"]) -> MetaOapg.properties.balance_floor: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["customer_type"]) -> MetaOapg.properties.customer_type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["financial_institution"]) -> 'FinancialInstitution': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["nickname"]) -> MetaOapg.properties.nickname: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["account_number", "account_status", "account_type", "balance_ceiling", "balance_floor", "creation_time", "currency", "customer_type", "financial_institution", "id", "last_updated_time", "nickname", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_number"]) -> typing.Union[MetaOapg.properties.account_number, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_status"]) -> typing.Union[MetaOapg.properties.account_status, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_type"]) -> typing.Union[MetaOapg.properties.account_type, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["balance_ceiling"]) -> typing.Union[MetaOapg.properties.balance_ceiling, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["balance_floor"]) -> typing.Union[MetaOapg.properties.balance_floor, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["creation_time"]) -> typing.Union[MetaOapg.properties.creation_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["currency"]) -> typing.Union[MetaOapg.properties.currency, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["customer_type"]) -> typing.Union[MetaOapg.properties.customer_type, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["financial_institution"]) -> typing.Union['FinancialInstitution', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_updated_time"]) -> typing.Union[MetaOapg.properties.last_updated_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["nickname"]) -> typing.Union[MetaOapg.properties.nickname, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["account_number", "account_status", "account_type", "balance_ceiling", "balance_floor", "creation_time", "currency", "customer_type", "financial_institution", "id", "last_updated_time", "nickname", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        account_number: typing.Union[MetaOapg.properties.account_number, str, schemas.Unset] = schemas.unset,
        account_status: typing.Union[MetaOapg.properties.account_status, str, schemas.Unset] = schemas.unset,
        account_type: typing.Union[MetaOapg.properties.account_type, str, schemas.Unset] = schemas.unset,
        balance_ceiling: typing.Union[MetaOapg.properties.balance_ceiling, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        balance_floor: typing.Union[MetaOapg.properties.balance_floor, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        creation_time: typing.Union[MetaOapg.properties.creation_time, str, datetime, schemas.Unset] = schemas.unset,
        currency: typing.Union[MetaOapg.properties.currency, str, schemas.Unset] = schemas.unset,
        customer_type: typing.Union[MetaOapg.properties.customer_type, str, schemas.Unset] = schemas.unset,
        financial_institution: typing.Union['FinancialInstitution', schemas.Unset] = schemas.unset,
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        last_updated_time: typing.Union[MetaOapg.properties.last_updated_time, str, datetime, schemas.Unset] = schemas.unset,
        nickname: typing.Union[MetaOapg.properties.nickname, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'AccountSummary':
        return super().__new__(
            cls,
            *_args,
            account_number=account_number,
            account_status=account_status,
            account_type=account_type,
            balance_ceiling=balance_ceiling,
            balance_floor=balance_floor,
            creation_time=creation_time,
            currency=currency,
            customer_type=customer_type,
            financial_institution=financial_institution,
            id=id,
            last_updated_time=last_updated_time,
            nickname=nickname,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.financial_institution import FinancialInstitution
