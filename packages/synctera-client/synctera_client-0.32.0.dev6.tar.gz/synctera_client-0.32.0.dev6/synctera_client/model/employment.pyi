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


class Employment(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    A period of time in which a customer is (was) employed by a particular employer.

    """


    class MetaOapg:
        required = {
            "employer_name",
        }
        
        class properties:
            employer_name = schemas.StrSchema
            employment_from = schemas.DateTimeSchema
            
            
            class employment_hours(
                schemas.Float32Schema
            ):
                pass
            employment_income = schemas.IntSchema
            employment_income_currency = schemas.StrSchema
            employment_info = schemas.DictSchema
            employment_occupation = schemas.StrSchema
            employment_to = schemas.DateTimeSchema
            id = schemas.UUIDSchema
            __annotations__ = {
                "employer_name": employer_name,
                "employment_from": employment_from,
                "employment_hours": employment_hours,
                "employment_income": employment_income,
                "employment_income_currency": employment_income_currency,
                "employment_info": employment_info,
                "employment_occupation": employment_occupation,
                "employment_to": employment_to,
                "id": id,
            }
    
    employer_name: MetaOapg.properties.employer_name
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["employer_name"]) -> MetaOapg.properties.employer_name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["employment_from"]) -> MetaOapg.properties.employment_from: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["employment_hours"]) -> MetaOapg.properties.employment_hours: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["employment_income"]) -> MetaOapg.properties.employment_income: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["employment_income_currency"]) -> MetaOapg.properties.employment_income_currency: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["employment_info"]) -> MetaOapg.properties.employment_info: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["employment_occupation"]) -> MetaOapg.properties.employment_occupation: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["employment_to"]) -> MetaOapg.properties.employment_to: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["employer_name", "employment_from", "employment_hours", "employment_income", "employment_income_currency", "employment_info", "employment_occupation", "employment_to", "id", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["employer_name"]) -> MetaOapg.properties.employer_name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["employment_from"]) -> typing.Union[MetaOapg.properties.employment_from, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["employment_hours"]) -> typing.Union[MetaOapg.properties.employment_hours, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["employment_income"]) -> typing.Union[MetaOapg.properties.employment_income, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["employment_income_currency"]) -> typing.Union[MetaOapg.properties.employment_income_currency, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["employment_info"]) -> typing.Union[MetaOapg.properties.employment_info, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["employment_occupation"]) -> typing.Union[MetaOapg.properties.employment_occupation, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["employment_to"]) -> typing.Union[MetaOapg.properties.employment_to, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["employer_name", "employment_from", "employment_hours", "employment_income", "employment_income_currency", "employment_info", "employment_occupation", "employment_to", "id", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        employer_name: typing.Union[MetaOapg.properties.employer_name, str, ],
        employment_from: typing.Union[MetaOapg.properties.employment_from, str, datetime, schemas.Unset] = schemas.unset,
        employment_hours: typing.Union[MetaOapg.properties.employment_hours, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        employment_income: typing.Union[MetaOapg.properties.employment_income, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        employment_income_currency: typing.Union[MetaOapg.properties.employment_income_currency, str, schemas.Unset] = schemas.unset,
        employment_info: typing.Union[MetaOapg.properties.employment_info, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        employment_occupation: typing.Union[MetaOapg.properties.employment_occupation, str, schemas.Unset] = schemas.unset,
        employment_to: typing.Union[MetaOapg.properties.employment_to, str, datetime, schemas.Unset] = schemas.unset,
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Employment':
        return super().__new__(
            cls,
            *_args,
            employer_name=employer_name,
            employment_from=employment_from,
            employment_hours=employment_hours,
            employment_income=employment_income,
            employment_income_currency=employment_income_currency,
            employment_info=employment_info,
            employment_occupation=employment_occupation,
            employment_to=employment_to,
            id=id,
            _configuration=_configuration,
            **kwargs,
        )
