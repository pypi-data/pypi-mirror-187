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


class CardProductUpdateRequest(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        class properties:
        
            @staticmethod
            def digital_wallet_tokenization() -> typing.Type['DigitalWalletTokenization']:
                return DigitalWalletTokenization
            issue_without_kyc = schemas.BoolSchema
            __annotations__ = {
                "digital_wallet_tokenization": digital_wallet_tokenization,
                "issue_without_kyc": issue_without_kyc,
            }
        additional_properties = schemas.NotAnyTypeSchema
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["digital_wallet_tokenization"]) -> 'DigitalWalletTokenization': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["issue_without_kyc"]) -> MetaOapg.properties.issue_without_kyc: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["digital_wallet_tokenization"], typing_extensions.Literal["issue_without_kyc"], ]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["digital_wallet_tokenization"]) -> typing.Union['DigitalWalletTokenization', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["issue_without_kyc"]) -> typing.Union[MetaOapg.properties.issue_without_kyc, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["digital_wallet_tokenization"], typing_extensions.Literal["issue_without_kyc"], ]):
        return super().get_item_oapg(name)

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        digital_wallet_tokenization: typing.Union['DigitalWalletTokenization', schemas.Unset] = schemas.unset,
        issue_without_kyc: typing.Union[MetaOapg.properties.issue_without_kyc, bool, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
    ) -> 'CardProductUpdateRequest':
        return super().__new__(
            cls,
            *_args,
            digital_wallet_tokenization=digital_wallet_tokenization,
            issue_without_kyc=issue_without_kyc,
            _configuration=_configuration,
        )

from synctera_client.model.digital_wallet_tokenization import DigitalWalletTokenization
