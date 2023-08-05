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


class Deposit(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Deposit using remote deposit capture
    """


    class MetaOapg:
        required = {
            "transaction_id",
            "deposit_amount",
            "account_id",
            "back_image_id",
            "deposit_currency",
            "front_image_id",
            "date_captured",
            "check_amount",
            "id",
            "date_processed",
            "vendor_info",
            "status",
        }
        
        class properties:
            account_id = schemas.UUIDSchema
            back_image_id = schemas.UUIDSchema
            
            
            class check_amount(
                schemas.IntSchema
            ):
            
            
                class MetaOapg:
                    inclusive_minimum = 1
            date_captured = schemas.DateTimeSchema
            date_processed = schemas.DateTimeSchema
            deposit_amount = schemas.IntSchema
            deposit_currency = schemas.StrSchema
            front_image_id = schemas.UUIDSchema
            id = schemas.UUIDSchema
            
            
            class status(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "SUBMITTED": "SUBMITTED",
                        "PENDING": "PENDING",
                        "FAILED": "FAILED",
                        "REJECTED": "REJECTED",
                    }
                
                @schemas.classproperty
                def SUBMITTED(cls):
                    return cls("SUBMITTED")
                
                @schemas.classproperty
                def PENDING(cls):
                    return cls("PENDING")
                
                @schemas.classproperty
                def FAILED(cls):
                    return cls("FAILED")
                
                @schemas.classproperty
                def REJECTED(cls):
                    return cls("REJECTED")
            transaction_id = schemas.UUIDSchema
        
            @staticmethod
            def vendor_info() -> typing.Type['VendorInfo1']:
                return VendorInfo1
            business_id = schemas.UUIDSchema
            creation_time = schemas.DateTimeSchema
            last_updated_time = schemas.DateTimeSchema
            metadata = schemas.DictSchema
            ocr_account_number = schemas.StrSchema
            ocr_check_number = schemas.StrSchema
            ocr_routing_number = schemas.StrSchema
            person_id = schemas.UUIDSchema
            __annotations__ = {
                "account_id": account_id,
                "back_image_id": back_image_id,
                "check_amount": check_amount,
                "date_captured": date_captured,
                "date_processed": date_processed,
                "deposit_amount": deposit_amount,
                "deposit_currency": deposit_currency,
                "front_image_id": front_image_id,
                "id": id,
                "status": status,
                "transaction_id": transaction_id,
                "vendor_info": vendor_info,
                "business_id": business_id,
                "creation_time": creation_time,
                "last_updated_time": last_updated_time,
                "metadata": metadata,
                "ocr_account_number": ocr_account_number,
                "ocr_check_number": ocr_check_number,
                "ocr_routing_number": ocr_routing_number,
                "person_id": person_id,
            }
    
    transaction_id: MetaOapg.properties.transaction_id
    deposit_amount: MetaOapg.properties.deposit_amount
    account_id: MetaOapg.properties.account_id
    back_image_id: MetaOapg.properties.back_image_id
    deposit_currency: MetaOapg.properties.deposit_currency
    front_image_id: MetaOapg.properties.front_image_id
    date_captured: MetaOapg.properties.date_captured
    check_amount: MetaOapg.properties.check_amount
    id: MetaOapg.properties.id
    date_processed: MetaOapg.properties.date_processed
    vendor_info: 'VendorInfo1'
    status: MetaOapg.properties.status
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account_id"]) -> MetaOapg.properties.account_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["back_image_id"]) -> MetaOapg.properties.back_image_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["check_amount"]) -> MetaOapg.properties.check_amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["date_captured"]) -> MetaOapg.properties.date_captured: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["date_processed"]) -> MetaOapg.properties.date_processed: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["deposit_amount"]) -> MetaOapg.properties.deposit_amount: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["deposit_currency"]) -> MetaOapg.properties.deposit_currency: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["front_image_id"]) -> MetaOapg.properties.front_image_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["transaction_id"]) -> MetaOapg.properties.transaction_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["vendor_info"]) -> 'VendorInfo1': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["business_id"]) -> MetaOapg.properties.business_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["ocr_account_number"]) -> MetaOapg.properties.ocr_account_number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["ocr_check_number"]) -> MetaOapg.properties.ocr_check_number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["ocr_routing_number"]) -> MetaOapg.properties.ocr_routing_number: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["person_id"]) -> MetaOapg.properties.person_id: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["account_id", "back_image_id", "check_amount", "date_captured", "date_processed", "deposit_amount", "deposit_currency", "front_image_id", "id", "status", "transaction_id", "vendor_info", "business_id", "creation_time", "last_updated_time", "metadata", "ocr_account_number", "ocr_check_number", "ocr_routing_number", "person_id", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account_id"]) -> MetaOapg.properties.account_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["back_image_id"]) -> MetaOapg.properties.back_image_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["check_amount"]) -> MetaOapg.properties.check_amount: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["date_captured"]) -> MetaOapg.properties.date_captured: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["date_processed"]) -> MetaOapg.properties.date_processed: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["deposit_amount"]) -> MetaOapg.properties.deposit_amount: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["deposit_currency"]) -> MetaOapg.properties.deposit_currency: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["front_image_id"]) -> MetaOapg.properties.front_image_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["transaction_id"]) -> MetaOapg.properties.transaction_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["vendor_info"]) -> 'VendorInfo1': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["business_id"]) -> typing.Union[MetaOapg.properties.business_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["creation_time"]) -> typing.Union[MetaOapg.properties.creation_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["last_updated_time"]) -> typing.Union[MetaOapg.properties.last_updated_time, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["ocr_account_number"]) -> typing.Union[MetaOapg.properties.ocr_account_number, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["ocr_check_number"]) -> typing.Union[MetaOapg.properties.ocr_check_number, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["ocr_routing_number"]) -> typing.Union[MetaOapg.properties.ocr_routing_number, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["person_id"]) -> typing.Union[MetaOapg.properties.person_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["account_id", "back_image_id", "check_amount", "date_captured", "date_processed", "deposit_amount", "deposit_currency", "front_image_id", "id", "status", "transaction_id", "vendor_info", "business_id", "creation_time", "last_updated_time", "metadata", "ocr_account_number", "ocr_check_number", "ocr_routing_number", "person_id", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        transaction_id: typing.Union[MetaOapg.properties.transaction_id, str, uuid.UUID, ],
        deposit_amount: typing.Union[MetaOapg.properties.deposit_amount, decimal.Decimal, int, ],
        account_id: typing.Union[MetaOapg.properties.account_id, str, uuid.UUID, ],
        back_image_id: typing.Union[MetaOapg.properties.back_image_id, str, uuid.UUID, ],
        deposit_currency: typing.Union[MetaOapg.properties.deposit_currency, str, ],
        front_image_id: typing.Union[MetaOapg.properties.front_image_id, str, uuid.UUID, ],
        date_captured: typing.Union[MetaOapg.properties.date_captured, str, datetime, ],
        check_amount: typing.Union[MetaOapg.properties.check_amount, decimal.Decimal, int, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        date_processed: typing.Union[MetaOapg.properties.date_processed, str, datetime, ],
        vendor_info: 'VendorInfo1',
        status: typing.Union[MetaOapg.properties.status, str, ],
        business_id: typing.Union[MetaOapg.properties.business_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        creation_time: typing.Union[MetaOapg.properties.creation_time, str, datetime, schemas.Unset] = schemas.unset,
        last_updated_time: typing.Union[MetaOapg.properties.last_updated_time, str, datetime, schemas.Unset] = schemas.unset,
        metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        ocr_account_number: typing.Union[MetaOapg.properties.ocr_account_number, str, schemas.Unset] = schemas.unset,
        ocr_check_number: typing.Union[MetaOapg.properties.ocr_check_number, str, schemas.Unset] = schemas.unset,
        ocr_routing_number: typing.Union[MetaOapg.properties.ocr_routing_number, str, schemas.Unset] = schemas.unset,
        person_id: typing.Union[MetaOapg.properties.person_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Deposit':
        return super().__new__(
            cls,
            *_args,
            transaction_id=transaction_id,
            deposit_amount=deposit_amount,
            account_id=account_id,
            back_image_id=back_image_id,
            deposit_currency=deposit_currency,
            front_image_id=front_image_id,
            date_captured=date_captured,
            check_amount=check_amount,
            id=id,
            date_processed=date_processed,
            vendor_info=vendor_info,
            status=status,
            business_id=business_id,
            creation_time=creation_time,
            last_updated_time=last_updated_time,
            metadata=metadata,
            ocr_account_number=ocr_account_number,
            ocr_check_number=ocr_check_number,
            ocr_routing_number=ocr_routing_number,
            person_id=person_id,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.vendor_info1 import VendorInfo1
