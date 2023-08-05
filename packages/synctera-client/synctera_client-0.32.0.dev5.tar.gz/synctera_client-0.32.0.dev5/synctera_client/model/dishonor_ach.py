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


class DishonorAch(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Dishonored return
    """


    class MetaOapg:
        required = {
            "type",
        }
        
        class properties:
            
            
            class type(
                schemas.EnumBase,
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    enum_value_to_name = {
                        "dishonored_misrouted": "MISROUTED",
                        "dishonored_erroneous_debit": "ERRONEOUS_DEBIT",
                        "dishonored_duplicate": "DUPLICATE",
                        "dishonored_untimely": "UNTIMELY",
                        "dishonored_field_errors": "FIELD_ERRORS",
                        "dishonored_not_requested": "NOT_REQUESTED",
                    }
                
                @schemas.classproperty
                def MISROUTED(cls):
                    return cls("dishonored_misrouted")
                
                @schemas.classproperty
                def ERRONEOUS_DEBIT(cls):
                    return cls("dishonored_erroneous_debit")
                
                @schemas.classproperty
                def DUPLICATE(cls):
                    return cls("dishonored_duplicate")
                
                @schemas.classproperty
                def UNTIMELY(cls):
                    return cls("dishonored_untimely")
                
                @schemas.classproperty
                def FIELD_ERRORS(cls):
                    return cls("dishonored_field_errors")
                
                @schemas.classproperty
                def NOT_REQUESTED(cls):
                    return cls("dishonored_not_requested")
            
            
            class field_errors(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    
                    class items(
                        schemas.EnumBase,
                        schemas.StrSchema
                    ):
                    
                    
                        class MetaOapg:
                            enum_value_to_name = {
                                "account_number": "ACCOUNT_NUMBER",
                                "original_trace_number": "ORIGINAL_TRACE_NUMBER",
                                "amount": "AMOUNT",
                                "identification_number": "IDENTIFICATION_NUMBER",
                                "transaction_code": "TRANSACTION_CODE",
                                "company_identification": "COMPANY_IDENTIFICATION",
                                "effective_date": "EFFECTIVE_DATE",
                            }
                        
                        @schemas.classproperty
                        def ACCOUNT_NUMBER(cls):
                            return cls("account_number")
                        
                        @schemas.classproperty
                        def ORIGINAL_TRACE_NUMBER(cls):
                            return cls("original_trace_number")
                        
                        @schemas.classproperty
                        def AMOUNT(cls):
                            return cls("amount")
                        
                        @schemas.classproperty
                        def IDENTIFICATION_NUMBER(cls):
                            return cls("identification_number")
                        
                        @schemas.classproperty
                        def TRANSACTION_CODE(cls):
                            return cls("transaction_code")
                        
                        @schemas.classproperty
                        def COMPANY_IDENTIFICATION(cls):
                            return cls("company_identification")
                        
                        @schemas.classproperty
                        def EFFECTIVE_DATE(cls):
                            return cls("effective_date")
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'field_errors':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            __annotations__ = {
                "type": type,
                "field_errors": field_errors,
            }
    
    type: MetaOapg.properties.type
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["field_errors"]) -> MetaOapg.properties.field_errors: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["type", "field_errors", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["field_errors"]) -> typing.Union[MetaOapg.properties.field_errors, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["type", "field_errors", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        type: typing.Union[MetaOapg.properties.type, str, ],
        field_errors: typing.Union[MetaOapg.properties.field_errors, list, tuple, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'DishonorAch':
        return super().__new__(
            cls,
            *_args,
            type=type,
            field_errors=field_errors,
            _configuration=_configuration,
            **kwargs,
        )
