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


class NoteResponse(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "creation_time",
            "related_resource_id",
            "last_updated_time",
            "author",
            "id",
            "related_resource_type",
            "content",
            "tenant",
        }
        
        class properties:
            author = schemas.StrSchema
            content = schemas.StrSchema
            creation_time = schemas.DateTimeSchema
            id = schemas.UUIDSchema
            last_updated_time = schemas.DateTimeSchema
            related_resource_id = schemas.StrSchema
        
            @staticmethod
            def related_resource_type() -> typing.Type['RelatedResourceType1']:
                return RelatedResourceType1
            tenant = schemas.StrSchema
            metadata = schemas.DictSchema
            __annotations__ = {
                "author": author,
                "content": content,
                "creation_time": creation_time,
                "id": id,
                "last_updated_time": last_updated_time,
                "related_resource_id": related_resource_id,
                "related_resource_type": related_resource_type,
                "tenant": tenant,
                "metadata": metadata,
            }
    
    creation_time: MetaOapg.properties.creation_time
    related_resource_id: MetaOapg.properties.related_resource_id
    last_updated_time: MetaOapg.properties.last_updated_time
    author: MetaOapg.properties.author
    id: MetaOapg.properties.id
    related_resource_type: 'RelatedResourceType1'
    content: MetaOapg.properties.content
    tenant: MetaOapg.properties.tenant
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["author"]) -> MetaOapg.properties.author: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["content"]) -> MetaOapg.properties.content: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["related_resource_id"]) -> MetaOapg.properties.related_resource_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["related_resource_type"]) -> 'RelatedResourceType1': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tenant"]) -> MetaOapg.properties.tenant: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["author", "content", "creation_time", "id", "last_updated_time", "related_resource_id", "related_resource_type", "tenant", "metadata", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["author"]) -> MetaOapg.properties.author: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["content"]) -> MetaOapg.properties.content: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["related_resource_id"]) -> MetaOapg.properties.related_resource_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["related_resource_type"]) -> 'RelatedResourceType1': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tenant"]) -> MetaOapg.properties.tenant: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["author", "content", "creation_time", "id", "last_updated_time", "related_resource_id", "related_resource_type", "tenant", "metadata", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        creation_time: typing.Union[MetaOapg.properties.creation_time, str, datetime, ],
        related_resource_id: typing.Union[MetaOapg.properties.related_resource_id, str, ],
        last_updated_time: typing.Union[MetaOapg.properties.last_updated_time, str, datetime, ],
        author: typing.Union[MetaOapg.properties.author, str, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        related_resource_type: 'RelatedResourceType1',
        content: typing.Union[MetaOapg.properties.content, str, ],
        tenant: typing.Union[MetaOapg.properties.tenant, str, ],
        metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'NoteResponse':
        return super().__new__(
            cls,
            *_args,
            creation_time=creation_time,
            related_resource_id=related_resource_id,
            last_updated_time=last_updated_time,
            author=author,
            id=id,
            related_resource_type=related_resource_type,
            content=content,
            tenant=tenant,
            metadata=metadata,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.related_resource_type1 import RelatedResourceType1
