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


class NoteCreate(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "related_resource_id",
            "related_resource_type",
            "content",
        }
        
        class properties:
            content = schemas.StrSchema
            related_resource_id = schemas.StrSchema
        
            @staticmethod
            def related_resource_type() -> typing.Type['RelatedResourceType1']:
                return RelatedResourceType1
            metadata = schemas.DictSchema
            tenant = schemas.StrSchema
            __annotations__ = {
                "content": content,
                "related_resource_id": related_resource_id,
                "related_resource_type": related_resource_type,
                "metadata": metadata,
                "tenant": tenant,
            }
    
    related_resource_id: MetaOapg.properties.related_resource_id
    related_resource_type: 'RelatedResourceType1'
    content: MetaOapg.properties.content
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["content"]) -> MetaOapg.properties.content: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["related_resource_id"]) -> MetaOapg.properties.related_resource_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["related_resource_type"]) -> 'RelatedResourceType1': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tenant"]) -> MetaOapg.properties.tenant: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["content", "related_resource_id", "related_resource_type", "metadata", "tenant", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["content"]) -> MetaOapg.properties.content: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["related_resource_id"]) -> MetaOapg.properties.related_resource_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["related_resource_type"]) -> 'RelatedResourceType1': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tenant"]) -> typing.Union[MetaOapg.properties.tenant, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["content", "related_resource_id", "related_resource_type", "metadata", "tenant", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        related_resource_id: typing.Union[MetaOapg.properties.related_resource_id, str, ],
        related_resource_type: 'RelatedResourceType1',
        content: typing.Union[MetaOapg.properties.content, str, ],
        metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        tenant: typing.Union[MetaOapg.properties.tenant, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'NoteCreate':
        return super().__new__(
            cls,
            *_args,
            related_resource_id=related_resource_id,
            related_resource_type=related_resource_type,
            content=content,
            metadata=metadata,
            tenant=tenant,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.related_resource_type1 import RelatedResourceType1
