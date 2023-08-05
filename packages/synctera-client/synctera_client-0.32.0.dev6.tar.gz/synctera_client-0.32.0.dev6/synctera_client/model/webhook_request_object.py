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


class WebhookRequestObject(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Request body for webhook http request
    """


    class MetaOapg:
        required = {
            "metadata",
            "webhook_id",
            "id",
            "type",
            "event_time",
            "url",
        }
        
        class properties:
            event_time = schemas.DateTimeSchema
            id = schemas.UUIDSchema
            
            
            class metadata(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 1024
        
            @staticmethod
            def type() -> typing.Type['EventTypeExplicit']:
                return EventTypeExplicit
            
            
            class url(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    format = 'uri'
                    max_length = 1000
            webhook_id = schemas.UUIDSchema
            event_resource = schemas.StrSchema
            event_resource_changed_fields = schemas.StrSchema
            
            
            class response_history(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['ResponseHistoryItem']:
                        return ResponseHistoryItem
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['ResponseHistoryItem'], typing.List['ResponseHistoryItem']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'response_history':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'ResponseHistoryItem':
                    return super().__getitem__(i)
            
            
            class status(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "RUNNING": "RUNNING",
                        "SUCCESS": "SUCCESS",
                        "RETRYING": "RETRYING",
                        "FAILED": "FAILED",
                    }
                
                @schemas.classproperty
                def RUNNING(cls):
                    return cls("RUNNING")
                
                @schemas.classproperty
                def SUCCESS(cls):
                    return cls("SUCCESS")
                
                @schemas.classproperty
                def RETRYING(cls):
                    return cls("RETRYING")
                
                @schemas.classproperty
                def FAILED(cls):
                    return cls("FAILED")
            __annotations__ = {
                "event_time": event_time,
                "id": id,
                "metadata": metadata,
                "type": type,
                "url": url,
                "webhook_id": webhook_id,
                "event_resource": event_resource,
                "event_resource_changed_fields": event_resource_changed_fields,
                "response_history": response_history,
                "status": status,
            }
    
    metadata: MetaOapg.properties.metadata
    webhook_id: MetaOapg.properties.webhook_id
    id: MetaOapg.properties.id
    type: 'EventTypeExplicit'
    event_time: MetaOapg.properties.event_time
    url: MetaOapg.properties.url
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["event_time"]) -> MetaOapg.properties.event_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["type"]) -> 'EventTypeExplicit': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["url"]) -> MetaOapg.properties.url: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["webhook_id"]) -> MetaOapg.properties.webhook_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["event_resource"]) -> MetaOapg.properties.event_resource: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["event_resource_changed_fields"]) -> MetaOapg.properties.event_resource_changed_fields: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["response_history"]) -> MetaOapg.properties.response_history: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["event_time", "id", "metadata", "type", "url", "webhook_id", "event_resource", "event_resource_changed_fields", "response_history", "status", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["event_time"]) -> MetaOapg.properties.event_time: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> 'EventTypeExplicit': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["url"]) -> MetaOapg.properties.url: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["webhook_id"]) -> MetaOapg.properties.webhook_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["event_resource"]) -> typing.Union[MetaOapg.properties.event_resource, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["event_resource_changed_fields"]) -> typing.Union[MetaOapg.properties.event_resource_changed_fields, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["response_history"]) -> typing.Union[MetaOapg.properties.response_history, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union[MetaOapg.properties.status, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["event_time", "id", "metadata", "type", "url", "webhook_id", "event_resource", "event_resource_changed_fields", "response_history", "status", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        metadata: typing.Union[MetaOapg.properties.metadata, str, ],
        webhook_id: typing.Union[MetaOapg.properties.webhook_id, str, uuid.UUID, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        type: 'EventTypeExplicit',
        event_time: typing.Union[MetaOapg.properties.event_time, str, datetime, ],
        url: typing.Union[MetaOapg.properties.url, str, ],
        event_resource: typing.Union[MetaOapg.properties.event_resource, str, schemas.Unset] = schemas.unset,
        event_resource_changed_fields: typing.Union[MetaOapg.properties.event_resource_changed_fields, str, schemas.Unset] = schemas.unset,
        response_history: typing.Union[MetaOapg.properties.response_history, list, tuple, schemas.Unset] = schemas.unset,
        status: typing.Union[MetaOapg.properties.status, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'WebhookRequestObject':
        return super().__new__(
            cls,
            *_args,
            metadata=metadata,
            webhook_id=webhook_id,
            id=id,
            type=type,
            event_time=event_time,
            url=url,
            event_resource=event_resource,
            event_resource_changed_fields=event_resource_changed_fields,
            response_history=response_history,
            status=status,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.event_type_explicit import EventTypeExplicit
from synctera_client.model.response_history_item import ResponseHistoryItem
