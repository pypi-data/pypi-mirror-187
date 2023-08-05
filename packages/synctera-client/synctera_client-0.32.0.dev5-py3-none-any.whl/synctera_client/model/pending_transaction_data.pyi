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


class PendingTransactionData(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "reason",
            "amount",
            "auto_post_at",
            "was_partial",
            "avail_balance",
            "idemkey",
            "memo",
            "history",
            "available_balance",
            "type",
            "network",
            "dc_sign",
            "force_post",
            "expires_at",
            "balance",
            "subtype",
            "total_amount",
            "effective_date",
            "transaction_time",
            "currency",
            "req_amount",
            "operation",
            "status",
        }
        
        class properties:
            
            
            class amount(
                schemas.Int64Schema
            ):
                pass
            auto_post_at = schemas.DateTimeSchema
            avail_balance = schemas.Int64Schema
            available_balance = schemas.Int64Schema
            balance = schemas.Int64Schema
            currency = schemas.StrSchema
        
            @staticmethod
            def dc_sign() -> typing.Type['DcSign']:
                return DcSign
            effective_date = schemas.DateTimeSchema
            expires_at = schemas.DateTimeSchema
            force_post = schemas.BoolSchema
            
            
            class history(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['PendingTransactionHistory']:
                        return PendingTransactionHistory
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['PendingTransactionHistory'], typing.List['PendingTransactionHistory']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'history':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'PendingTransactionHistory':
                    return super().__getitem__(i)
            idemkey = schemas.StrSchema
            memo = schemas.StrSchema
            network = schemas.StrSchema
            
            
            class operation(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def NEW(cls):
                    return cls("hold_new")
                
                @schemas.classproperty
                def INCREASE(cls):
                    return cls("hold_increase")
                
                @schemas.classproperty
                def DECREASE(cls):
                    return cls("hold_decrease")
                
                @schemas.classproperty
                def REPLACE(cls):
                    return cls("hold_replace")
                
                @schemas.classproperty
                def DECLINE(cls):
                    return cls("hold_decline")
                
                @schemas.classproperty
                def CANCEL(cls):
                    return cls("hold_cancel")
                
                @schemas.classproperty
                def POST(cls):
                    return cls("hold_post")
                
                @schemas.classproperty
                def EXPIRE(cls):
                    return cls("hold_expire")
            reason = schemas.StrSchema
            
            
            class req_amount(
                schemas.Int64Schema
            ):
                pass
            
            
            class status(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def PENDING(cls):
                    return cls("PENDING")
                
                @schemas.classproperty
                def REPLACED(cls):
                    return cls("REPLACED")
                
                @schemas.classproperty
                def DECLINED(cls):
                    return cls("DECLINED")
                
                @schemas.classproperty
                def RELEASED(cls):
                    return cls("RELEASED")
                
                @schemas.classproperty
                def PARTCLEARED(cls):
                    return cls("PARTCLEARED")
                
                @schemas.classproperty
                def EXPIRED(cls):
                    return cls("EXPIRED")
                
                @schemas.classproperty
                def CLEARED(cls):
                    return cls("CLEARED")
                
                @schemas.classproperty
                def INTERNAL_ERROR(cls):
                    return cls("INTERNAL_ERROR")
            subtype = schemas.StrSchema
            
            
            class total_amount(
                schemas.Int64Schema
            ):
                pass
            transaction_time = schemas.DateTimeSchema
            type = schemas.StrSchema
            was_partial = schemas.BoolSchema
            
            
            class external_data(
                schemas.DictBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneFrozenDictMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'external_data':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class risk_info(
                schemas.DictBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneFrozenDictMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'risk_info':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            transaction_id = schemas.UUIDSchema
            
            
            class user_data(
                schemas.DictBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneFrozenDictMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'user_data':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            __annotations__ = {
                "amount": amount,
                "auto_post_at": auto_post_at,
                "avail_balance": avail_balance,
                "available_balance": available_balance,
                "balance": balance,
                "currency": currency,
                "dc_sign": dc_sign,
                "effective_date": effective_date,
                "expires_at": expires_at,
                "force_post": force_post,
                "history": history,
                "idemkey": idemkey,
                "memo": memo,
                "network": network,
                "operation": operation,
                "reason": reason,
                "req_amount": req_amount,
                "status": status,
                "subtype": subtype,
                "total_amount": total_amount,
                "transaction_time": transaction_time,
                "type": type,
                "was_partial": was_partial,
                "external_data": external_data,
                "risk_info": risk_info,
                "transaction_id": transaction_id,
                "user_data": user_data,
            }
    
    reason: MetaOapg.properties.reason
    amount: MetaOapg.properties.amount
    auto_post_at: MetaOapg.properties.auto_post_at
    was_partial: MetaOapg.properties.was_partial
    avail_balance: MetaOapg.properties.avail_balance
    idemkey: MetaOapg.properties.idemkey
    memo: MetaOapg.properties.memo
    history: MetaOapg.properties.history
    available_balance: MetaOapg.properties.available_balance
    type: MetaOapg.properties.type
    network: MetaOapg.properties.network
    dc_sign: 'DcSign'
    force_post: MetaOapg.properties.force_post
    expires_at: MetaOapg.properties.expires_at
    balance: MetaOapg.properties.balance
    subtype: MetaOapg.properties.subtype
    total_amount: MetaOapg.properties.total_amount
    effective_date: MetaOapg.properties.effective_date
    transaction_time: MetaOapg.properties.transaction_time
    currency: MetaOapg.properties.currency
    req_amount: MetaOapg.properties.req_amount
    operation: MetaOapg.properties.operation
    status: MetaOapg.properties.status
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["auto_post_at"]) -> MetaOapg.properties.auto_post_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["avail_balance"]) -> MetaOapg.properties.avail_balance: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["available_balance"]) -> MetaOapg.properties.available_balance: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["balance"]) -> MetaOapg.properties.balance: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["dc_sign"]) -> 'DcSign': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["effective_date"]) -> MetaOapg.properties.effective_date: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["expires_at"]) -> MetaOapg.properties.expires_at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["force_post"]) -> MetaOapg.properties.force_post: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["history"]) -> MetaOapg.properties.history: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["idemkey"]) -> MetaOapg.properties.idemkey: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["memo"]) -> MetaOapg.properties.memo: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["network"]) -> MetaOapg.properties.network: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["operation"]) -> MetaOapg.properties.operation: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["reason"]) -> MetaOapg.properties.reason: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["req_amount"]) -> MetaOapg.properties.req_amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["subtype"]) -> MetaOapg.properties.subtype: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["total_amount"]) -> MetaOapg.properties.total_amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["transaction_time"]) -> MetaOapg.properties.transaction_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["was_partial"]) -> MetaOapg.properties.was_partial: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["external_data"]) -> MetaOapg.properties.external_data: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["risk_info"]) -> MetaOapg.properties.risk_info: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["transaction_id"]) -> MetaOapg.properties.transaction_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["user_data"]) -> MetaOapg.properties.user_data: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["amount", "auto_post_at", "avail_balance", "available_balance", "balance", "currency", "dc_sign", "effective_date", "expires_at", "force_post", "history", "idemkey", "memo", "network", "operation", "reason", "req_amount", "status", "subtype", "total_amount", "transaction_time", "type", "was_partial", "external_data", "risk_info", "transaction_id", "user_data", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["amount"]) -> MetaOapg.properties.amount: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["auto_post_at"]) -> MetaOapg.properties.auto_post_at: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["avail_balance"]) -> MetaOapg.properties.avail_balance: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["available_balance"]) -> MetaOapg.properties.available_balance: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["balance"]) -> MetaOapg.properties.balance: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["currency"]) -> MetaOapg.properties.currency: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["dc_sign"]) -> 'DcSign': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["effective_date"]) -> MetaOapg.properties.effective_date: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["expires_at"]) -> MetaOapg.properties.expires_at: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["force_post"]) -> MetaOapg.properties.force_post: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["history"]) -> MetaOapg.properties.history: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["idemkey"]) -> MetaOapg.properties.idemkey: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["memo"]) -> MetaOapg.properties.memo: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["network"]) -> MetaOapg.properties.network: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["operation"]) -> MetaOapg.properties.operation: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["reason"]) -> MetaOapg.properties.reason: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["req_amount"]) -> MetaOapg.properties.req_amount: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["subtype"]) -> MetaOapg.properties.subtype: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["total_amount"]) -> MetaOapg.properties.total_amount: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["transaction_time"]) -> MetaOapg.properties.transaction_time: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["was_partial"]) -> MetaOapg.properties.was_partial: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["external_data"]) -> typing.Union[MetaOapg.properties.external_data, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["risk_info"]) -> typing.Union[MetaOapg.properties.risk_info, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["transaction_id"]) -> typing.Union[MetaOapg.properties.transaction_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["user_data"]) -> typing.Union[MetaOapg.properties.user_data, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["amount", "auto_post_at", "avail_balance", "available_balance", "balance", "currency", "dc_sign", "effective_date", "expires_at", "force_post", "history", "idemkey", "memo", "network", "operation", "reason", "req_amount", "status", "subtype", "total_amount", "transaction_time", "type", "was_partial", "external_data", "risk_info", "transaction_id", "user_data", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        reason: typing.Union[MetaOapg.properties.reason, str, ],
        amount: typing.Union[MetaOapg.properties.amount, decimal.Decimal, int, ],
        auto_post_at: typing.Union[MetaOapg.properties.auto_post_at, str, datetime, ],
        was_partial: typing.Union[MetaOapg.properties.was_partial, bool, ],
        avail_balance: typing.Union[MetaOapg.properties.avail_balance, decimal.Decimal, int, ],
        idemkey: typing.Union[MetaOapg.properties.idemkey, str, ],
        memo: typing.Union[MetaOapg.properties.memo, str, ],
        history: typing.Union[MetaOapg.properties.history, list, tuple, ],
        available_balance: typing.Union[MetaOapg.properties.available_balance, decimal.Decimal, int, ],
        type: typing.Union[MetaOapg.properties.type, str, ],
        network: typing.Union[MetaOapg.properties.network, str, ],
        dc_sign: 'DcSign',
        force_post: typing.Union[MetaOapg.properties.force_post, bool, ],
        expires_at: typing.Union[MetaOapg.properties.expires_at, str, datetime, ],
        balance: typing.Union[MetaOapg.properties.balance, decimal.Decimal, int, ],
        subtype: typing.Union[MetaOapg.properties.subtype, str, ],
        total_amount: typing.Union[MetaOapg.properties.total_amount, decimal.Decimal, int, ],
        effective_date: typing.Union[MetaOapg.properties.effective_date, str, datetime, ],
        transaction_time: typing.Union[MetaOapg.properties.transaction_time, str, datetime, ],
        currency: typing.Union[MetaOapg.properties.currency, str, ],
        req_amount: typing.Union[MetaOapg.properties.req_amount, decimal.Decimal, int, ],
        operation: typing.Union[MetaOapg.properties.operation, str, ],
        status: typing.Union[MetaOapg.properties.status, str, ],
        external_data: typing.Union[MetaOapg.properties.external_data, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        risk_info: typing.Union[MetaOapg.properties.risk_info, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        transaction_id: typing.Union[MetaOapg.properties.transaction_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        user_data: typing.Union[MetaOapg.properties.user_data, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'PendingTransactionData':
        return super().__new__(
            cls,
            *_args,
            reason=reason,
            amount=amount,
            auto_post_at=auto_post_at,
            was_partial=was_partial,
            avail_balance=avail_balance,
            idemkey=idemkey,
            memo=memo,
            history=history,
            available_balance=available_balance,
            type=type,
            network=network,
            dc_sign=dc_sign,
            force_post=force_post,
            expires_at=expires_at,
            balance=balance,
            subtype=subtype,
            total_amount=total_amount,
            effective_date=effective_date,
            transaction_time=transaction_time,
            currency=currency,
            req_amount=req_amount,
            operation=operation,
            status=status,
            external_data=external_data,
            risk_info=risk_info,
            transaction_id=transaction_id,
            user_data=user_data,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.dc_sign import DcSign
from synctera_client.model.pending_transaction_history import PendingTransactionHistory
