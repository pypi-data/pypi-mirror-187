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


class CustomerVerification(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "customer_consent",
        }
        
        class properties:
            customer_consent = schemas.BoolSchema
            
            
            class customer_ip_address(
                schemas.StrSchema
            ):
                pass
            document_id = schemas.StrSchema
            
            
            class verification_type(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['VerificationType']:
                        return VerificationType
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['VerificationType'], typing.List['VerificationType']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'verification_type':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'VerificationType':
                    return super().__getitem__(i)
            __annotations__ = {
                "customer_consent": customer_consent,
                "customer_ip_address": customer_ip_address,
                "document_id": document_id,
                "verification_type": verification_type,
            }
    
    customer_consent: MetaOapg.properties.customer_consent
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["customer_consent"]) -> MetaOapg.properties.customer_consent: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["customer_ip_address"]) -> MetaOapg.properties.customer_ip_address: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["document_id"]) -> MetaOapg.properties.document_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["verification_type"]) -> MetaOapg.properties.verification_type: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["customer_consent", "customer_ip_address", "document_id", "verification_type", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["customer_consent"]) -> MetaOapg.properties.customer_consent: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["customer_ip_address"]) -> typing.Union[MetaOapg.properties.customer_ip_address, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["document_id"]) -> typing.Union[MetaOapg.properties.document_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["verification_type"]) -> typing.Union[MetaOapg.properties.verification_type, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["customer_consent", "customer_ip_address", "document_id", "verification_type", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        customer_consent: typing.Union[MetaOapg.properties.customer_consent, bool, ],
        customer_ip_address: typing.Union[MetaOapg.properties.customer_ip_address, str, schemas.Unset] = schemas.unset,
        document_id: typing.Union[MetaOapg.properties.document_id, str, schemas.Unset] = schemas.unset,
        verification_type: typing.Union[MetaOapg.properties.verification_type, list, tuple, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CustomerVerification':
        return super().__new__(
            cls,
            *_args,
            customer_consent=customer_consent,
            customer_ip_address=customer_ip_address,
            document_id=document_id,
            verification_type=verification_type,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.verification_type import VerificationType
