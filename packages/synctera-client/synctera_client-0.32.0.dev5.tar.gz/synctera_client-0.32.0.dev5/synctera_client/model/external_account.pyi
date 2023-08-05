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


class ExternalAccount(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "creation_time",
            "last_updated_time",
            "routing_identifiers",
            "account_owner_names",
            "id",
            "type",
            "account_identifiers",
            "verification",
            "status",
        }
        
        class properties:
        
            @staticmethod
            def account_identifiers() -> typing.Type['AccountIdentifiers']:
                return AccountIdentifiers
            
            
            class account_owner_names(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.StrSchema
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'account_owner_names':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            creation_time = schemas.DateTimeSchema
            id = schemas.UUIDSchema
            last_updated_time = schemas.DateTimeSchema
        
            @staticmethod
            def routing_identifiers() -> typing.Type['AccountRouting']:
                return AccountRouting
            
            
            class status(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def ACTIVE(cls):
                    return cls("ACTIVE")
                
                @schemas.classproperty
                def CLOSED(cls):
                    return cls("CLOSED")
            
            
            class type(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def CHECKING(cls):
                    return cls("CHECKING")
                
                @schemas.classproperty
                def SAVINGS(cls):
                    return cls("SAVINGS")
                
                @schemas.classproperty
                def CREDIT_CARD(cls):
                    return cls("CREDIT_CARD")
                
                @schemas.classproperty
                def MONEY_MARKET(cls):
                    return cls("MONEY_MARKET")
                
                @schemas.classproperty
                def INVESTMENT_529(cls):
                    return cls("INVESTMENT_529")
                
                @schemas.classproperty
                def OTHER(cls):
                    return cls("OTHER")
        
            @staticmethod
            def verification() -> typing.Type['AccountVerification']:
                return AccountVerification
            business_id = schemas.UUIDSchema
            customer_id = schemas.UUIDSchema
            deletion_time = schemas.DateTimeSchema
            metadata = schemas.DictSchema
            name = schemas.StrSchema
            
            
            class nickname(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'nickname':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
        
            @staticmethod
            def vendor_data() -> typing.Type['ExternalAccountVendorData']:
                return ExternalAccountVendorData
        
            @staticmethod
            def vendor_info() -> typing.Type['VendorInfo']:
                return VendorInfo
            __annotations__ = {
                "account_identifiers": account_identifiers,
                "account_owner_names": account_owner_names,
                "creation_time": creation_time,
                "id": id,
                "last_updated_time": last_updated_time,
                "routing_identifiers": routing_identifiers,
                "status": status,
                "type": type,
                "verification": verification,
                "business_id": business_id,
                "customer_id": customer_id,
                "deletion_time": deletion_time,
                "metadata": metadata,
                "name": name,
                "nickname": nickname,
                "vendor_data": vendor_data,
                "vendor_info": vendor_info,
            }
    
    creation_time: MetaOapg.properties.creation_time
    last_updated_time: MetaOapg.properties.last_updated_time
    routing_identifiers: 'AccountRouting'
    account_owner_names: MetaOapg.properties.account_owner_names
    id: MetaOapg.properties.id
    type: MetaOapg.properties.type
    account_identifiers: 'AccountIdentifiers'
    verification: 'AccountVerification'
    status: MetaOapg.properties.status
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_identifiers"]) -> 'AccountIdentifiers': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_owner_names"]) -> MetaOapg.properties.account_owner_names: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["routing_identifiers"]) -> 'AccountRouting': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["verification"]) -> 'AccountVerification': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["business_id"]) -> MetaOapg.properties.business_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["customer_id"]) -> MetaOapg.properties.customer_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["deletion_time"]) -> MetaOapg.properties.deletion_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["nickname"]) -> MetaOapg.properties.nickname: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["vendor_data"]) -> 'ExternalAccountVendorData': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["vendor_info"]) -> 'VendorInfo': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["account_identifiers", "account_owner_names", "creation_time", "id", "last_updated_time", "routing_identifiers", "status", "type", "verification", "business_id", "customer_id", "deletion_time", "metadata", "name", "nickname", "vendor_data", "vendor_info", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_identifiers"]) -> 'AccountIdentifiers': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_owner_names"]) -> MetaOapg.properties.account_owner_names: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["routing_identifiers"]) -> 'AccountRouting': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["verification"]) -> 'AccountVerification': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["business_id"]) -> typing.Union[MetaOapg.properties.business_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["customer_id"]) -> typing.Union[MetaOapg.properties.customer_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["deletion_time"]) -> typing.Union[MetaOapg.properties.deletion_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["nickname"]) -> typing.Union[MetaOapg.properties.nickname, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["vendor_data"]) -> typing.Union['ExternalAccountVendorData', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["vendor_info"]) -> typing.Union['VendorInfo', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["account_identifiers", "account_owner_names", "creation_time", "id", "last_updated_time", "routing_identifiers", "status", "type", "verification", "business_id", "customer_id", "deletion_time", "metadata", "name", "nickname", "vendor_data", "vendor_info", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        creation_time: typing.Union[MetaOapg.properties.creation_time, str, datetime, ],
        last_updated_time: typing.Union[MetaOapg.properties.last_updated_time, str, datetime, ],
        routing_identifiers: 'AccountRouting',
        account_owner_names: typing.Union[MetaOapg.properties.account_owner_names, list, tuple, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        type: typing.Union[MetaOapg.properties.type, str, ],
        account_identifiers: 'AccountIdentifiers',
        verification: 'AccountVerification',
        status: typing.Union[MetaOapg.properties.status, str, ],
        business_id: typing.Union[MetaOapg.properties.business_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        customer_id: typing.Union[MetaOapg.properties.customer_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        deletion_time: typing.Union[MetaOapg.properties.deletion_time, str, datetime, schemas.Unset] = schemas.unset,
        metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
        nickname: typing.Union[MetaOapg.properties.nickname, None, str, schemas.Unset] = schemas.unset,
        vendor_data: typing.Union['ExternalAccountVendorData', schemas.Unset] = schemas.unset,
        vendor_info: typing.Union['VendorInfo', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ExternalAccount':
        return super().__new__(
            cls,
            *_args,
            creation_time=creation_time,
            last_updated_time=last_updated_time,
            routing_identifiers=routing_identifiers,
            account_owner_names=account_owner_names,
            id=id,
            type=type,
            account_identifiers=account_identifiers,
            verification=verification,
            status=status,
            business_id=business_id,
            customer_id=customer_id,
            deletion_time=deletion_time,
            metadata=metadata,
            name=name,
            nickname=nickname,
            vendor_data=vendor_data,
            vendor_info=vendor_info,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.account_identifiers import AccountIdentifiers
from synctera_client.model.account_routing import AccountRouting
from synctera_client.model.account_verification import AccountVerification
from synctera_client.model.external_account_vendor_data import ExternalAccountVendorData
from synctera_client.model.vendor_info import VendorInfo
