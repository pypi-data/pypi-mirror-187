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


class VerificationVendorXml(
    schemas.AnyTypeSchema,
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "content_type",
            "vendor",
            "xml",
        }
        
        class properties:
            
            
            class content_type(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def TEXT_XML(cls):
                    return cls("text/xml")
            vendor = schemas.StrSchema
            xml = schemas.StrSchema
            
            
            class details(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['VerificationVendorInfoDetail']:
                        return VerificationVendorInfoDetail
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['VerificationVendorInfoDetail'], typing.List['VerificationVendorInfoDetail']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'details':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'VerificationVendorInfoDetail':
                    return super().__getitem__(i)
            __annotations__ = {
                "content_type": content_type,
                "vendor": vendor,
                "xml": xml,
                "details": details,
            }

    
    content_type: MetaOapg.properties.content_type
    vendor: MetaOapg.properties.vendor
    xml: MetaOapg.properties.xml
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["content_type"]) -> MetaOapg.properties.content_type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["vendor"]) -> MetaOapg.properties.vendor: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["xml"]) -> MetaOapg.properties.xml: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["details"]) -> MetaOapg.properties.details: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["content_type", "vendor", "xml", "details", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["content_type"]) -> MetaOapg.properties.content_type: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["vendor"]) -> MetaOapg.properties.vendor: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["xml"]) -> MetaOapg.properties.xml: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["details"]) -> typing.Union[MetaOapg.properties.details, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["content_type", "vendor", "xml", "details", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
        content_type: typing.Union[MetaOapg.properties.content_type, str, ],
        vendor: typing.Union[MetaOapg.properties.vendor, str, ],
        xml: typing.Union[MetaOapg.properties.xml, str, ],
        details: typing.Union[MetaOapg.properties.details, list, tuple, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'VerificationVendorXml':
        return super().__new__(
            cls,
            *_args,
            content_type=content_type,
            vendor=vendor,
            xml=xml,
            details=details,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.verification_vendor_info_detail import VerificationVendorInfoDetail
