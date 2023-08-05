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


class PhysicalCardResponseStatus(
    schemas.ComposedSchema,
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        
        class all_of_1(
            schemas.DictSchema
        ):
        
        
            class MetaOapg:
                required = {
                    "card_status",
                    "card_fulfillment_status",
                    "status_reason",
                }
                
                class properties:
                
                    @staticmethod
                    def card_fulfillment_status() -> typing.Type['CardFulfillmentStatus']:
                        return CardFulfillmentStatus
                
                    @staticmethod
                    def fulfillment_details() -> typing.Type['FulfillmentDetails']:
                        return FulfillmentDetails
                    tracking_number = schemas.StrSchema
                    __annotations__ = {
                        "card_fulfillment_status": card_fulfillment_status,
                        "fulfillment_details": fulfillment_details,
                        "tracking_number": tracking_number,
                    }
            
            card_status: schemas.AnyTypeSchema
            card_fulfillment_status: 'CardFulfillmentStatus'
            status_reason: schemas.AnyTypeSchema
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["card_fulfillment_status"]) -> 'CardFulfillmentStatus': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["fulfillment_details"]) -> 'FulfillmentDetails': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["tracking_number"]) -> MetaOapg.properties.tracking_number: ...
            
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            
            def __getitem__(self, name: typing.Union[typing_extensions.Literal["card_fulfillment_status", "fulfillment_details", "tracking_number", ], str]):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["card_fulfillment_status"]) -> 'CardFulfillmentStatus': ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["fulfillment_details"]) -> typing.Union['FulfillmentDetails', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["tracking_number"]) -> typing.Union[MetaOapg.properties.tracking_number, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            
            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["card_fulfillment_status", "fulfillment_details", "tracking_number", ], str]):
                return super().get_item_oapg(name)
            
        
            def __new__(
                cls,
                *_args: typing.Union[dict, frozendict.frozendict, ],
                card_status: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                card_fulfillment_status: 'CardFulfillmentStatus',
                status_reason: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                fulfillment_details: typing.Union['FulfillmentDetails', schemas.Unset] = schemas.unset,
                tracking_number: typing.Union[MetaOapg.properties.tracking_number, str, schemas.Unset] = schemas.unset,
                _configuration: typing.Optional[schemas.Configuration] = None,
                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
            ) -> 'all_of_1':
                return super().__new__(
                    cls,
                    *_args,
                    card_status=card_status,
                    card_fulfillment_status=card_fulfillment_status,
                    status_reason=status_reason,
                    fulfillment_details=fulfillment_details,
                    tracking_number=tracking_number,
                    _configuration=_configuration,
                    **kwargs,
                )
        
        @classmethod
        @functools.lru_cache()
        def all_of(cls):
            # we need this here to make our import statements work
            # we must store _composed_schemas in here so the code is only run
            # when we invoke this method. If we kept this at the class
            # level we would get an error because the class level
            # code would be run when this module is imported, and these composed
            # classes don't exist yet because their module has not finished
            # loading
            return [
                CardStatusObject,
                cls.all_of_1,
            ]


    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'PhysicalCardResponseStatus':
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.card_fulfillment_status import CardFulfillmentStatus
from synctera_client.model.card_status_object import CardStatusObject
from synctera_client.model.fulfillment_details import FulfillmentDetails
