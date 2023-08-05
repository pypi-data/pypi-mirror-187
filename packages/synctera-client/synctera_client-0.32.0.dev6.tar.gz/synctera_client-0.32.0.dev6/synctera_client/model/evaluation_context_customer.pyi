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


class EvaluationContextCustomer(
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
            "resource_type",
        }
        
        class properties:
            bank_id = schemas.IntSchema
            partner_id = schemas.IntSchema
        
            @staticmethod
            def resource_type() -> typing.Type['ResourceType']:
                return ResourceType
            email = schemas.StrSchema
            
            
            class phone_number(
                schemas.StrSchema
            ):
                pass
            ssn_token = schemas.StrSchema
            __annotations__ = {
                "bank_id": bank_id,
                "partner_id": partner_id,
                "resource_type": resource_type,
                "email": email,
                "phone_number": phone_number,
                "ssn_token": ssn_token,
            }
    
    partner_id: MetaOapg.properties.partner_id
    bank_id: MetaOapg.properties.bank_id
    resource_type: 'ResourceType'
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["bank_id"]) -> MetaOapg.properties.bank_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["partner_id"]) -> MetaOapg.properties.partner_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["resource_type"]) -> 'ResourceType': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["email"]) -> MetaOapg.properties.email: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["phone_number"]) -> MetaOapg.properties.phone_number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["ssn_token"]) -> MetaOapg.properties.ssn_token: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["bank_id", "partner_id", "resource_type", "email", "phone_number", "ssn_token", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["bank_id"]) -> MetaOapg.properties.bank_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["partner_id"]) -> MetaOapg.properties.partner_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["resource_type"]) -> 'ResourceType': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["email"]) -> typing.Union[MetaOapg.properties.email, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["phone_number"]) -> typing.Union[MetaOapg.properties.phone_number, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["ssn_token"]) -> typing.Union[MetaOapg.properties.ssn_token, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["bank_id", "partner_id", "resource_type", "email", "phone_number", "ssn_token", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        partner_id: typing.Union[MetaOapg.properties.partner_id, decimal.Decimal, int, ],
        bank_id: typing.Union[MetaOapg.properties.bank_id, decimal.Decimal, int, ],
        resource_type: 'ResourceType',
        email: typing.Union[MetaOapg.properties.email, str, schemas.Unset] = schemas.unset,
        phone_number: typing.Union[MetaOapg.properties.phone_number, str, schemas.Unset] = schemas.unset,
        ssn_token: typing.Union[MetaOapg.properties.ssn_token, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'EvaluationContextCustomer':
        return super().__new__(
            cls,
            *_args,
            partner_id=partner_id,
            bank_id=bank_id,
            resource_type=resource_type,
            email=email,
            phone_number=phone_number,
            ssn_token=ssn_token,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.resource_type import ResourceType
