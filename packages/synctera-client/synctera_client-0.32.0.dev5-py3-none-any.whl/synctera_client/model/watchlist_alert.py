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


class WatchlistAlert(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "status",
        }
        
        class properties:
            
            
            class status(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "ACTIVE": "ACTIVE",
                        "SUPPRESSED": "SUPPRESSED",
                    }
                
                @schemas.classproperty
                def ACTIVE(cls):
                    return cls("ACTIVE")
                
                @schemas.classproperty
                def SUPPRESSED(cls):
                    return cls("SUPPRESSED")
            created = schemas.DateTimeSchema
            id = schemas.UUIDSchema
            provider_info = schemas.DictSchema
            provider_subject_id = schemas.StrSchema
            provider_subscription_id = schemas.StrSchema
            provider_watchlist_name = schemas.StrSchema
            
            
            class urls(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.StrSchema
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'urls':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
        
            @staticmethod
            def vendor_info() -> typing.Type['VendorInfo']:
                return VendorInfo
            __annotations__ = {
                "status": status,
                "created": created,
                "id": id,
                "provider_info": provider_info,
                "provider_subject_id": provider_subject_id,
                "provider_subscription_id": provider_subscription_id,
                "provider_watchlist_name": provider_watchlist_name,
                "urls": urls,
                "vendor_info": vendor_info,
            }
    
    status: MetaOapg.properties.status
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["created"]) -> MetaOapg.properties.created: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["provider_info"]) -> MetaOapg.properties.provider_info: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["provider_subject_id"]) -> MetaOapg.properties.provider_subject_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["provider_subscription_id"]) -> MetaOapg.properties.provider_subscription_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["provider_watchlist_name"]) -> MetaOapg.properties.provider_watchlist_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["urls"]) -> MetaOapg.properties.urls: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["vendor_info"]) -> 'VendorInfo': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["status", "created", "id", "provider_info", "provider_subject_id", "provider_subscription_id", "provider_watchlist_name", "urls", "vendor_info", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["created"]) -> typing.Union[MetaOapg.properties.created, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["provider_info"]) -> typing.Union[MetaOapg.properties.provider_info, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["provider_subject_id"]) -> typing.Union[MetaOapg.properties.provider_subject_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["provider_subscription_id"]) -> typing.Union[MetaOapg.properties.provider_subscription_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["provider_watchlist_name"]) -> typing.Union[MetaOapg.properties.provider_watchlist_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["urls"]) -> typing.Union[MetaOapg.properties.urls, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["vendor_info"]) -> typing.Union['VendorInfo', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["status", "created", "id", "provider_info", "provider_subject_id", "provider_subscription_id", "provider_watchlist_name", "urls", "vendor_info", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        status: typing.Union[MetaOapg.properties.status, str, ],
        created: typing.Union[MetaOapg.properties.created, str, datetime, schemas.Unset] = schemas.unset,
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        provider_info: typing.Union[MetaOapg.properties.provider_info, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        provider_subject_id: typing.Union[MetaOapg.properties.provider_subject_id, str, schemas.Unset] = schemas.unset,
        provider_subscription_id: typing.Union[MetaOapg.properties.provider_subscription_id, str, schemas.Unset] = schemas.unset,
        provider_watchlist_name: typing.Union[MetaOapg.properties.provider_watchlist_name, str, schemas.Unset] = schemas.unset,
        urls: typing.Union[MetaOapg.properties.urls, list, tuple, schemas.Unset] = schemas.unset,
        vendor_info: typing.Union['VendorInfo', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'WatchlistAlert':
        return super().__new__(
            cls,
            *_args,
            status=status,
            created=created,
            id=id,
            provider_info=provider_info,
            provider_subject_id=provider_subject_id,
            provider_subscription_id=provider_subscription_id,
            provider_watchlist_name=provider_watchlist_name,
            urls=urls,
            vendor_info=vendor_info,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.vendor_info import VendorInfo
