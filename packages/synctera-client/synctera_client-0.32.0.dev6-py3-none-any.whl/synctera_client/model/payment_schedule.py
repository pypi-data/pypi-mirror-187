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


class PaymentSchedule(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Payment schedule
    """


    class MetaOapg:
        required = {
            "schedule",
            "description",
            "payment_instruction",
        }
        
        class properties:
            description = schemas.StrSchema
        
            @staticmethod
            def payment_instruction() -> typing.Type['PaymentInstruction']:
                return PaymentInstruction
        
            @staticmethod
            def schedule() -> typing.Type['ScheduleConfig']:
                return ScheduleConfig
            id = schemas.UUIDSchema
            metadata = schemas.DictSchema
        
            @staticmethod
            def next_payment_date() -> typing.Type['PaymentDate']:
                return PaymentDate
        
            @staticmethod
            def status() -> typing.Type['PaymentScheduleStatus']:
                return PaymentScheduleStatus
            __annotations__ = {
                "description": description,
                "payment_instruction": payment_instruction,
                "schedule": schedule,
                "id": id,
                "metadata": metadata,
                "next_payment_date": next_payment_date,
                "status": status,
            }
    
    schedule: 'ScheduleConfig'
    description: MetaOapg.properties.description
    payment_instruction: 'PaymentInstruction'
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["payment_instruction"]) -> 'PaymentInstruction': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["schedule"]) -> 'ScheduleConfig': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["next_payment_date"]) -> 'PaymentDate': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> 'PaymentScheduleStatus': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["description", "payment_instruction", "schedule", "id", "metadata", "next_payment_date", "status", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["payment_instruction"]) -> 'PaymentInstruction': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["schedule"]) -> 'ScheduleConfig': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["next_payment_date"]) -> typing.Union['PaymentDate', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union['PaymentScheduleStatus', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["description", "payment_instruction", "schedule", "id", "metadata", "next_payment_date", "status", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        schedule: 'ScheduleConfig',
        description: typing.Union[MetaOapg.properties.description, str, ],
        payment_instruction: 'PaymentInstruction',
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        next_payment_date: typing.Union['PaymentDate', schemas.Unset] = schemas.unset,
        status: typing.Union['PaymentScheduleStatus', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'PaymentSchedule':
        return super().__new__(
            cls,
            *_args,
            schedule=schedule,
            description=description,
            payment_instruction=payment_instruction,
            id=id,
            metadata=metadata,
            next_payment_date=next_payment_date,
            status=status,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.payment_date import PaymentDate
from synctera_client.model.payment_instruction import PaymentInstruction
from synctera_client.model.payment_schedule_status import PaymentScheduleStatus
from synctera_client.model.schedule_config import ScheduleConfig
