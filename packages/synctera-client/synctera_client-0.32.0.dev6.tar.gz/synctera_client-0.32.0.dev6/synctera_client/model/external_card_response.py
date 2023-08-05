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


class ExternalCardResponse(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "expiration_year",
            "last_four",
            "expiration_month",
            "name",
            "currency",
            "id",
            "customer_id",
        }
        
        class properties:
        
            @staticmethod
            def currency() -> typing.Type['CurrencyCode']:
                return CurrencyCode
            customer_id = schemas.UUIDSchema
            expiration_month = schemas.StrSchema
            expiration_year = schemas.StrSchema
            id = schemas.StrSchema
            last_four = schemas.StrSchema
            name = schemas.StrSchema
            created_time = schemas.DateTimeSchema
            last_modified_time = schemas.DateTimeSchema
        
            @staticmethod
            def verifications() -> typing.Type['ExternalCardVerifications']:
                return ExternalCardVerifications
            __annotations__ = {
                "currency": currency,
                "customer_id": customer_id,
                "expiration_month": expiration_month,
                "expiration_year": expiration_year,
                "id": id,
                "last_four": last_four,
                "name": name,
                "created_time": created_time,
                "last_modified_time": last_modified_time,
                "verifications": verifications,
            }
    
    expiration_year: MetaOapg.properties.expiration_year
    last_four: MetaOapg.properties.last_four
    expiration_month: MetaOapg.properties.expiration_month
    name: MetaOapg.properties.name
    currency: 'CurrencyCode'
    id: MetaOapg.properties.id
    customer_id: MetaOapg.properties.customer_id
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["currency"]) -> 'CurrencyCode': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["customer_id"]) -> MetaOapg.properties.customer_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["expiration_month"]) -> MetaOapg.properties.expiration_month: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["expiration_year"]) -> MetaOapg.properties.expiration_year: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_four"]) -> MetaOapg.properties.last_four: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["created_time"]) -> MetaOapg.properties.created_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_modified_time"]) -> MetaOapg.properties.last_modified_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["verifications"]) -> 'ExternalCardVerifications': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["currency", "customer_id", "expiration_month", "expiration_year", "id", "last_four", "name", "created_time", "last_modified_time", "verifications", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["currency"]) -> 'CurrencyCode': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["customer_id"]) -> MetaOapg.properties.customer_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["expiration_month"]) -> MetaOapg.properties.expiration_month: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["expiration_year"]) -> MetaOapg.properties.expiration_year: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_four"]) -> MetaOapg.properties.last_four: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["created_time"]) -> typing.Union[MetaOapg.properties.created_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_modified_time"]) -> typing.Union[MetaOapg.properties.last_modified_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["verifications"]) -> typing.Union['ExternalCardVerifications', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["currency", "customer_id", "expiration_month", "expiration_year", "id", "last_four", "name", "created_time", "last_modified_time", "verifications", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        expiration_year: typing.Union[MetaOapg.properties.expiration_year, str, ],
        last_four: typing.Union[MetaOapg.properties.last_four, str, ],
        expiration_month: typing.Union[MetaOapg.properties.expiration_month, str, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        currency: 'CurrencyCode',
        id: typing.Union[MetaOapg.properties.id, str, ],
        customer_id: typing.Union[MetaOapg.properties.customer_id, str, uuid.UUID, ],
        created_time: typing.Union[MetaOapg.properties.created_time, str, datetime, schemas.Unset] = schemas.unset,
        last_modified_time: typing.Union[MetaOapg.properties.last_modified_time, str, datetime, schemas.Unset] = schemas.unset,
        verifications: typing.Union['ExternalCardVerifications', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ExternalCardResponse':
        return super().__new__(
            cls,
            *_args,
            expiration_year=expiration_year,
            last_four=last_four,
            expiration_month=expiration_month,
            name=name,
            currency=currency,
            id=id,
            customer_id=customer_id,
            created_time=created_time,
            last_modified_time=last_modified_time,
            verifications=verifications,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.currency_code import CurrencyCode
from synctera_client.model.external_card_verifications import ExternalCardVerifications
