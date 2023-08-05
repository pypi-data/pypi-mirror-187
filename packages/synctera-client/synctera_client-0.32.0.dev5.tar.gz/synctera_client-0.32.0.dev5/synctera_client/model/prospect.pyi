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


class Prospect(
    schemas.ComposedBase,
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    A prospect has a unique identifier. It can be upgrade to a customer with required information
    """


    class MetaOapg:
        
        
        class all_of_0(
            schemas.AnyTypeSchema,
        ):
        
        
            class MetaOapg:
                required = {
                    "status",
                }
                
                class properties:
                    dob = schemas.DateSchema
                    first_name = schemas.StrSchema
                    last_name = schemas.StrSchema
                    
                    
                    class status(
                        schemas.EnumBase,
                        schemas.StrSchema
                    ):
                        
                        @schemas.classproperty
                        def ACTIVE(cls):
                            return cls("ACTIVE")
                        
                        @schemas.classproperty
                        def ESCHEAT(cls):
                            return cls("ESCHEAT")
                        
                        @schemas.classproperty
                        def DECEASED(cls):
                            return cls("DECEASED")
                        
                        @schemas.classproperty
                        def DENIED(cls):
                            return cls("DENIED")
                        
                        @schemas.classproperty
                        def DORMANT(cls):
                            return cls("DORMANT")
                        
                        @schemas.classproperty
                        def FROZEN(cls):
                            return cls("FROZEN")
                        
                        @schemas.classproperty
                        def INACTIVE(cls):
                            return cls("INACTIVE")
                        
                        @schemas.classproperty
                        def PROSPECT(cls):
                            return cls("PROSPECT")
                        
                        @schemas.classproperty
                        def SANCTION(cls):
                            return cls("SANCTION")
                    __annotations__ = {
                        "dob": dob,
                        "first_name": first_name,
                        "last_name": last_name,
                        "status": status,
                    }
        
            
            status: MetaOapg.properties.status
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["dob"]) -> MetaOapg.properties.dob: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["first_name"]) -> MetaOapg.properties.first_name: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["last_name"]) -> MetaOapg.properties.last_name: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
            
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            
            def __getitem__(self, name: typing.Union[typing_extensions.Literal["dob", "first_name", "last_name", "status", ], str]):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["dob"]) -> typing.Union[MetaOapg.properties.dob, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["first_name"]) -> typing.Union[MetaOapg.properties.first_name, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["last_name"]) -> typing.Union[MetaOapg.properties.last_name, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
            
            @typing.overload
            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            
            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["dob", "first_name", "last_name", "status", ], str]):
                return super().get_item_oapg(name)
            
        
            def __new__(
                cls,
                *_args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                status: typing.Union[MetaOapg.properties.status, str, ],
                dob: typing.Union[MetaOapg.properties.dob, str, date, schemas.Unset] = schemas.unset,
                first_name: typing.Union[MetaOapg.properties.first_name, str, schemas.Unset] = schemas.unset,
                last_name: typing.Union[MetaOapg.properties.last_name, str, schemas.Unset] = schemas.unset,
                _configuration: typing.Optional[schemas.Configuration] = None,
                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
            ) -> 'all_of_0':
                return super().__new__(
                    cls,
                    *_args,
                    status=status,
                    dob=dob,
                    first_name=first_name,
                    last_name=last_name,
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
                cls.all_of_0,
                BasePerson,
            ]


    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Prospect':
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.base_person import BasePerson
