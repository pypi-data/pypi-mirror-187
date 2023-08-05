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


class AddVendorAccountsErrorReason(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    A machine-readable code describing the reason for the failure.
    """


    class MetaOapg:
        enum_value_to_name = {
            "FAILED_VERIFICATION": "FAILED_VERIFICATION",
            "UNSUPPORTED_ACCOUNT_TYPE": "UNSUPPORTED_ACCOUNT_TYPE",
            "DUPLICATE_ACCOUNT": "DUPLICATE_ACCOUNT",
            "ACCOUNT_NOT_FOUND": "ACCOUNT_NOT_FOUND",
            "PROVIDER_ERROR": "PROVIDER_ERROR",
        }
    
    @schemas.classproperty
    def FAILED_VERIFICATION(cls):
        return cls("FAILED_VERIFICATION")
    
    @schemas.classproperty
    def UNSUPPORTED_ACCOUNT_TYPE(cls):
        return cls("UNSUPPORTED_ACCOUNT_TYPE")
    
    @schemas.classproperty
    def DUPLICATE_ACCOUNT(cls):
        return cls("DUPLICATE_ACCOUNT")
    
    @schemas.classproperty
    def ACCOUNT_NOT_FOUND(cls):
        return cls("ACCOUNT_NOT_FOUND")
    
    @schemas.classproperty
    def PROVIDER_ERROR(cls):
        return cls("PROVIDER_ERROR")
