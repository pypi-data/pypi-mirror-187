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


class CardProgram(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "partner_id",
            "bank_id",
            "card_category",
            "card_brand",
            "name",
            "card_product_type",
        }
        
        class properties:
            bank_id = schemas.IntSchema
        
            @staticmethod
            def card_brand() -> typing.Type['CardBrand']:
                return CardBrand
        
            @staticmethod
            def card_category() -> typing.Type['CardCategory']:
                return CardCategory
        
            @staticmethod
            def card_product_type() -> typing.Type['CardProductType']:
                return CardProductType
            name = schemas.StrSchema
            partner_id = schemas.IntSchema
            active = schemas.BoolSchema
            creation_time = schemas.DateTimeSchema
            end_date = schemas.DateTimeSchema
            id = schemas.UUIDSchema
            last_modified_time = schemas.DateTimeSchema
            start_date = schemas.DateTimeSchema
            __annotations__ = {
                "bank_id": bank_id,
                "card_brand": card_brand,
                "card_category": card_category,
                "card_product_type": card_product_type,
                "name": name,
                "partner_id": partner_id,
                "active": active,
                "creation_time": creation_time,
                "end_date": end_date,
                "id": id,
                "last_modified_time": last_modified_time,
                "start_date": start_date,
            }
    
    partner_id: MetaOapg.properties.partner_id
    bank_id: MetaOapg.properties.bank_id
    card_category: 'CardCategory'
    card_brand: 'CardBrand'
    name: MetaOapg.properties.name
    card_product_type: 'CardProductType'
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bank_id"]) -> MetaOapg.properties.bank_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["card_brand"]) -> 'CardBrand': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["card_category"]) -> 'CardCategory': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["card_product_type"]) -> 'CardProductType': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["partner_id"]) -> MetaOapg.properties.partner_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["active"]) -> MetaOapg.properties.active: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["end_date"]) -> MetaOapg.properties.end_date: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_modified_time"]) -> MetaOapg.properties.last_modified_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["start_date"]) -> MetaOapg.properties.start_date: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["bank_id", "card_brand", "card_category", "card_product_type", "name", "partner_id", "active", "creation_time", "end_date", "id", "last_modified_time", "start_date", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bank_id"]) -> MetaOapg.properties.bank_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["card_brand"]) -> 'CardBrand': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["card_category"]) -> 'CardCategory': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["card_product_type"]) -> 'CardProductType': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["partner_id"]) -> MetaOapg.properties.partner_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["active"]) -> typing.Union[MetaOapg.properties.active, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["creation_time"]) -> typing.Union[MetaOapg.properties.creation_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["end_date"]) -> typing.Union[MetaOapg.properties.end_date, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_modified_time"]) -> typing.Union[MetaOapg.properties.last_modified_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["start_date"]) -> typing.Union[MetaOapg.properties.start_date, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["bank_id", "card_brand", "card_category", "card_product_type", "name", "partner_id", "active", "creation_time", "end_date", "id", "last_modified_time", "start_date", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        partner_id: typing.Union[MetaOapg.properties.partner_id, decimal.Decimal, int, ],
        bank_id: typing.Union[MetaOapg.properties.bank_id, decimal.Decimal, int, ],
        card_category: 'CardCategory',
        card_brand: 'CardBrand',
        name: typing.Union[MetaOapg.properties.name, str, ],
        card_product_type: 'CardProductType',
        active: typing.Union[MetaOapg.properties.active, bool, schemas.Unset] = schemas.unset,
        creation_time: typing.Union[MetaOapg.properties.creation_time, str, datetime, schemas.Unset] = schemas.unset,
        end_date: typing.Union[MetaOapg.properties.end_date, str, datetime, schemas.Unset] = schemas.unset,
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        last_modified_time: typing.Union[MetaOapg.properties.last_modified_time, str, datetime, schemas.Unset] = schemas.unset,
        start_date: typing.Union[MetaOapg.properties.start_date, str, datetime, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CardProgram':
        return super().__new__(
            cls,
            *_args,
            partner_id=partner_id,
            bank_id=bank_id,
            card_category=card_category,
            card_brand=card_brand,
            name=name,
            card_product_type=card_product_type,
            active=active,
            creation_time=creation_time,
            end_date=end_date,
            id=id,
            last_modified_time=last_modified_time,
            start_date=start_date,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.card_brand import CardBrand
from synctera_client.model.card_category import CardCategory
from synctera_client.model.card_product_type import CardProductType
