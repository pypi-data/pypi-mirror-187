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


class BaseCard(
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
                    "form",
                }
                
                class properties:
                    account_id = schemas.UUIDSchema
                    card_product_id = schemas.UUIDSchema
                    creation_time = schemas.DateTimeSchema
                    customer_id = schemas.UUIDSchema
                
                    @staticmethod
                    def emboss_name() -> typing.Type['EmbossName']:
                        return EmbossName
                    expiration_month = schemas.StrSchema
                    expiration_time = schemas.DateTimeSchema
                    expiration_year = schemas.StrSchema
                    id = schemas.UUIDSchema
                    is_pin_set = schemas.BoolSchema
                    last_four = schemas.StrSchema
                    last_modified_time = schemas.DateTimeSchema
                
                    @staticmethod
                    def metadata() -> typing.Type['CardMetadata']:
                        return CardMetadata
                    
                    
                    class reissue_reason(
                        schemas.EnumBase,
                        schemas.StrSchema
                    ):
                        
                        @schemas.classproperty
                        def EXPIRATION(cls):
                            return cls("EXPIRATION")
                        
                        @schemas.classproperty
                        def LOST(cls):
                            return cls("LOST")
                        
                        @schemas.classproperty
                        def STOLEN(cls):
                            return cls("STOLEN")
                        
                        @schemas.classproperty
                        def DAMAGED(cls):
                            return cls("DAMAGED")
                        
                        @schemas.classproperty
                        def NAME_CHANGE(cls):
                            return cls("NAME_CHANGE")
                        
                        @schemas.classproperty
                        def VIRTUAL_TO_PHYSICAL(cls):
                            return cls("VIRTUAL_TO_PHYSICAL")
                        
                        @schemas.classproperty
                        def PRODUCT_CHANGE(cls):
                            return cls("PRODUCT_CHANGE")
                        
                        @schemas.classproperty
                        def APPEARANCE(cls):
                            return cls("APPEARANCE")
                    reissued_from_id = schemas.UUIDSchema
                    reissued_to_id = schemas.UUIDSchema
                    
                    
                    class type(
                        schemas.EnumBase,
                        schemas.StrSchema
                    ):
                        
                        @schemas.classproperty
                        def DEBIT(cls):
                            return cls("DEBIT")
                    __annotations__ = {
                        "account_id": account_id,
                        "card_product_id": card_product_id,
                        "creation_time": creation_time,
                        "customer_id": customer_id,
                        "emboss_name": emboss_name,
                        "expiration_month": expiration_month,
                        "expiration_time": expiration_time,
                        "expiration_year": expiration_year,
                        "id": id,
                        "is_pin_set": is_pin_set,
                        "last_four": last_four,
                        "last_modified_time": last_modified_time,
                        "metadata": metadata,
                        "reissue_reason": reissue_reason,
                        "reissued_from_id": reissued_from_id,
                        "reissued_to_id": reissued_to_id,
                        "type": type,
                    }
            
            form: schemas.AnyTypeSchema
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["account_id"]) -> MetaOapg.properties.account_id: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["card_product_id"]) -> MetaOapg.properties.card_product_id: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["customer_id"]) -> MetaOapg.properties.customer_id: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["emboss_name"]) -> 'EmbossName': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["expiration_month"]) -> MetaOapg.properties.expiration_month: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["expiration_time"]) -> MetaOapg.properties.expiration_time: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["expiration_year"]) -> MetaOapg.properties.expiration_year: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["is_pin_set"]) -> MetaOapg.properties.is_pin_set: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["last_four"]) -> MetaOapg.properties.last_four: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["last_modified_time"]) -> MetaOapg.properties.last_modified_time: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> 'CardMetadata': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["reissue_reason"]) -> MetaOapg.properties.reissue_reason: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["reissued_from_id"]) -> MetaOapg.properties.reissued_from_id: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["reissued_to_id"]) -> MetaOapg.properties.reissued_to_id: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
            
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            
            def __getitem__(self, name: typing.Union[typing_extensions.Literal["account_id", "card_product_id", "creation_time", "customer_id", "emboss_name", "expiration_month", "expiration_time", "expiration_year", "id", "is_pin_set", "last_four", "last_modified_time", "metadata", "reissue_reason", "reissued_from_id", "reissued_to_id", "type", ], str]):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["account_id"]) -> typing.Union[MetaOapg.properties.account_id, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["card_product_id"]) -> typing.Union[MetaOapg.properties.card_product_id, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["creation_time"]) -> typing.Union[MetaOapg.properties.creation_time, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["customer_id"]) -> typing.Union[MetaOapg.properties.customer_id, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["emboss_name"]) -> typing.Union['EmbossName', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["expiration_month"]) -> typing.Union[MetaOapg.properties.expiration_month, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["expiration_time"]) -> typing.Union[MetaOapg.properties.expiration_time, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["expiration_year"]) -> typing.Union[MetaOapg.properties.expiration_year, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["is_pin_set"]) -> typing.Union[MetaOapg.properties.is_pin_set, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["last_four"]) -> typing.Union[MetaOapg.properties.last_four, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["last_modified_time"]) -> typing.Union[MetaOapg.properties.last_modified_time, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union['CardMetadata', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["reissue_reason"]) -> typing.Union[MetaOapg.properties.reissue_reason, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["reissued_from_id"]) -> typing.Union[MetaOapg.properties.reissued_from_id, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["reissued_to_id"]) -> typing.Union[MetaOapg.properties.reissued_to_id, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> typing.Union[MetaOapg.properties.type, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            
            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["account_id", "card_product_id", "creation_time", "customer_id", "emboss_name", "expiration_month", "expiration_time", "expiration_year", "id", "is_pin_set", "last_four", "last_modified_time", "metadata", "reissue_reason", "reissued_from_id", "reissued_to_id", "type", ], str]):
                return super().get_item_oapg(name)
            
        
            def __new__(
                cls,
                *_args: typing.Union[dict, frozendict.frozendict, ],
                form: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                account_id: typing.Union[MetaOapg.properties.account_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
                card_product_id: typing.Union[MetaOapg.properties.card_product_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
                creation_time: typing.Union[MetaOapg.properties.creation_time, str, datetime, schemas.Unset] = schemas.unset,
                customer_id: typing.Union[MetaOapg.properties.customer_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
                emboss_name: typing.Union['EmbossName', schemas.Unset] = schemas.unset,
                expiration_month: typing.Union[MetaOapg.properties.expiration_month, str, schemas.Unset] = schemas.unset,
                expiration_time: typing.Union[MetaOapg.properties.expiration_time, str, datetime, schemas.Unset] = schemas.unset,
                expiration_year: typing.Union[MetaOapg.properties.expiration_year, str, schemas.Unset] = schemas.unset,
                id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
                is_pin_set: typing.Union[MetaOapg.properties.is_pin_set, bool, schemas.Unset] = schemas.unset,
                last_four: typing.Union[MetaOapg.properties.last_four, str, schemas.Unset] = schemas.unset,
                last_modified_time: typing.Union[MetaOapg.properties.last_modified_time, str, datetime, schemas.Unset] = schemas.unset,
                metadata: typing.Union['CardMetadata', schemas.Unset] = schemas.unset,
                reissue_reason: typing.Union[MetaOapg.properties.reissue_reason, str, schemas.Unset] = schemas.unset,
                reissued_from_id: typing.Union[MetaOapg.properties.reissued_from_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
                reissued_to_id: typing.Union[MetaOapg.properties.reissued_to_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
                type: typing.Union[MetaOapg.properties.type, str, schemas.Unset] = schemas.unset,
                _configuration: typing.Optional[schemas.Configuration] = None,
                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
            ) -> 'all_of_1':
                return super().__new__(
                    cls,
                    *_args,
                    form=form,
                    account_id=account_id,
                    card_product_id=card_product_id,
                    creation_time=creation_time,
                    customer_id=customer_id,
                    emboss_name=emboss_name,
                    expiration_month=expiration_month,
                    expiration_time=expiration_time,
                    expiration_year=expiration_year,
                    id=id,
                    is_pin_set=is_pin_set,
                    last_four=last_four,
                    last_modified_time=last_modified_time,
                    metadata=metadata,
                    reissue_reason=reissue_reason,
                    reissued_from_id=reissued_from_id,
                    reissued_to_id=reissued_to_id,
                    type=type,
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
                CardFormat,
                cls.all_of_1,
            ]


    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'BaseCard':
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.card_format import CardFormat
from synctera_client.model.card_metadata import CardMetadata
from synctera_client.model.emboss_name import EmbossName
