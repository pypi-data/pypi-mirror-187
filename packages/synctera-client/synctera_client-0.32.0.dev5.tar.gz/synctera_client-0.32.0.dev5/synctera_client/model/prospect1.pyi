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


class Prospect1(
    schemas.ComposedSchema,
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        
        class all_of_0(
            schemas.DictSchema
        ):
        
        
            class MetaOapg:
                required = {
                    "email",
                }
                
                class properties:
                    creation_time = schemas.DateTimeSchema
                    email = schemas.StrSchema
                    
                    
                    class email_validation(
                        schemas.EnumBase,
                        schemas.StrSchema
                    ):
                        
                        @schemas.classproperty
                        def PENDING(cls):
                            return cls("PENDING")
                        
                        @schemas.classproperty
                        def VALID(cls):
                            return cls("VALID")
                        
                        @schemas.classproperty
                        def INVALID(cls):
                            return cls("INVALID")
                    id = schemas.UUIDSchema
                    last_updated_time = schemas.DateTimeSchema
                    points = schemas.IntSchema
                    recaptcha_token = schemas.StrSchema
                    referral_code = schemas.StrSchema
                    referred_by = schemas.UUIDSchema
                    referred_by_code = schemas.StrSchema
                    referred_prospects = schemas.IntSchema
                
                    @staticmethod
                    def vendor_info() -> typing.Type['VendorInfo']:
                        return VendorInfo
                    verification_token = schemas.StrSchema
                    waitlist_id = schemas.UUIDSchema
                    
                    
                    class waitlist_position(
                        schemas.IntBase,
                        schemas.NoneBase,
                        schemas.Schema,
                        schemas.NoneDecimalMixin
                    ):
                    
                    
                        def __new__(
                            cls,
                            *_args: typing.Union[None, decimal.Decimal, int, ],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                        ) -> 'waitlist_position':
                            return super().__new__(
                                cls,
                                *_args,
                                _configuration=_configuration,
                            )
                    __annotations__ = {
                        "creation_time": creation_time,
                        "email": email,
                        "email_validation": email_validation,
                        "id": id,
                        "last_updated_time": last_updated_time,
                        "points": points,
                        "recaptcha_token": recaptcha_token,
                        "referral_code": referral_code,
                        "referred_by": referred_by,
                        "referred_by_code": referred_by_code,
                        "referred_prospects": referred_prospects,
                        "vendor_info": vendor_info,
                        "verification_token": verification_token,
                        "waitlist_id": waitlist_id,
                        "waitlist_position": waitlist_position,
                    }
            
            email: MetaOapg.properties.email
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["creation_time"]) -> MetaOapg.properties.creation_time: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["email"]) -> MetaOapg.properties.email: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["email_validation"]) -> MetaOapg.properties.email_validation: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["last_updated_time"]) -> MetaOapg.properties.last_updated_time: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["points"]) -> MetaOapg.properties.points: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["recaptcha_token"]) -> MetaOapg.properties.recaptcha_token: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["referral_code"]) -> MetaOapg.properties.referral_code: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["referred_by"]) -> MetaOapg.properties.referred_by: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["referred_by_code"]) -> MetaOapg.properties.referred_by_code: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["referred_prospects"]) -> MetaOapg.properties.referred_prospects: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["vendor_info"]) -> 'VendorInfo': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["verification_token"]) -> MetaOapg.properties.verification_token: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["waitlist_id"]) -> MetaOapg.properties.waitlist_id: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["waitlist_position"]) -> MetaOapg.properties.waitlist_position: ...
            
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            
            def __getitem__(self, name: typing.Union[typing_extensions.Literal["creation_time", "email", "email_validation", "id", "last_updated_time", "points", "recaptcha_token", "referral_code", "referred_by", "referred_by_code", "referred_prospects", "vendor_info", "verification_token", "waitlist_id", "waitlist_position", ], str]):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["creation_time"]) -> typing.Union[MetaOapg.properties.creation_time, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["email"]) -> MetaOapg.properties.email: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["email_validation"]) -> typing.Union[MetaOapg.properties.email_validation, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> typing.Union[MetaOapg.properties.id, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["last_updated_time"]) -> typing.Union[MetaOapg.properties.last_updated_time, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["points"]) -> typing.Union[MetaOapg.properties.points, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["recaptcha_token"]) -> typing.Union[MetaOapg.properties.recaptcha_token, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["referral_code"]) -> typing.Union[MetaOapg.properties.referral_code, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["referred_by"]) -> typing.Union[MetaOapg.properties.referred_by, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["referred_by_code"]) -> typing.Union[MetaOapg.properties.referred_by_code, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["referred_prospects"]) -> typing.Union[MetaOapg.properties.referred_prospects, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["vendor_info"]) -> typing.Union['VendorInfo', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["verification_token"]) -> typing.Union[MetaOapg.properties.verification_token, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["waitlist_id"]) -> typing.Union[MetaOapg.properties.waitlist_id, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["waitlist_position"]) -> typing.Union[MetaOapg.properties.waitlist_position, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            
            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["creation_time", "email", "email_validation", "id", "last_updated_time", "points", "recaptcha_token", "referral_code", "referred_by", "referred_by_code", "referred_prospects", "vendor_info", "verification_token", "waitlist_id", "waitlist_position", ], str]):
                return super().get_item_oapg(name)
            
        
            def __new__(
                cls,
                *_args: typing.Union[dict, frozendict.frozendict, ],
                email: typing.Union[MetaOapg.properties.email, str, ],
                creation_time: typing.Union[MetaOapg.properties.creation_time, str, datetime, schemas.Unset] = schemas.unset,
                email_validation: typing.Union[MetaOapg.properties.email_validation, str, schemas.Unset] = schemas.unset,
                id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, schemas.Unset] = schemas.unset,
                last_updated_time: typing.Union[MetaOapg.properties.last_updated_time, str, datetime, schemas.Unset] = schemas.unset,
                points: typing.Union[MetaOapg.properties.points, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                recaptcha_token: typing.Union[MetaOapg.properties.recaptcha_token, str, schemas.Unset] = schemas.unset,
                referral_code: typing.Union[MetaOapg.properties.referral_code, str, schemas.Unset] = schemas.unset,
                referred_by: typing.Union[MetaOapg.properties.referred_by, str, uuid.UUID, schemas.Unset] = schemas.unset,
                referred_by_code: typing.Union[MetaOapg.properties.referred_by_code, str, schemas.Unset] = schemas.unset,
                referred_prospects: typing.Union[MetaOapg.properties.referred_prospects, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                vendor_info: typing.Union['VendorInfo', schemas.Unset] = schemas.unset,
                verification_token: typing.Union[MetaOapg.properties.verification_token, str, schemas.Unset] = schemas.unset,
                waitlist_id: typing.Union[MetaOapg.properties.waitlist_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
                waitlist_position: typing.Union[MetaOapg.properties.waitlist_position, None, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                _configuration: typing.Optional[schemas.Configuration] = None,
                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
            ) -> 'all_of_0':
                return super().__new__(
                    cls,
                    *_args,
                    email=email,
                    creation_time=creation_time,
                    email_validation=email_validation,
                    id=id,
                    last_updated_time=last_updated_time,
                    points=points,
                    recaptcha_token=recaptcha_token,
                    referral_code=referral_code,
                    referred_by=referred_by,
                    referred_by_code=referred_by_code,
                    referred_prospects=referred_prospects,
                    vendor_info=vendor_info,
                    verification_token=verification_token,
                    waitlist_id=waitlist_id,
                    waitlist_position=waitlist_position,
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
                ProspectEditable,
            ]


    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Prospect1':
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.prospect_editable import ProspectEditable
from synctera_client.model.vendor_info import VendorInfo
