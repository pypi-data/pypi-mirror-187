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


class VerificationResult(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    The determination of this verification. One of the following:
* `UNVERIFIED` – record representing the absence of a verification.
* `PENDING` – verification is in progress for this customer.
* `PROVISIONAL` – partially verified or verified with restrictions.
* `ACCEPTED` – the customer has been verified.
* `REVIEW` – verification has run and issues have been identified and require review.
* `VENDOR_ERROR` – verification did not successfully run due to an unexpected error or failure.
* `REJECTED` – the customer was rejected and should not be allowed to take certain actions e.g., open an account.

    """


    class MetaOapg:
        enum_value_to_name = {
            "UNVERIFIED": "UNVERIFIED",
            "PENDING": "PENDING",
            "PROVISIONAL": "PROVISIONAL",
            "ACCEPTED": "ACCEPTED",
            "REVIEW": "REVIEW",
            "VENDOR_ERROR": "VENDOR_ERROR",
            "REJECTED": "REJECTED",
        }
    
    @schemas.classproperty
    def UNVERIFIED(cls):
        return cls("UNVERIFIED")
    
    @schemas.classproperty
    def PENDING(cls):
        return cls("PENDING")
    
    @schemas.classproperty
    def PROVISIONAL(cls):
        return cls("PROVISIONAL")
    
    @schemas.classproperty
    def ACCEPTED(cls):
        return cls("ACCEPTED")
    
    @schemas.classproperty
    def REVIEW(cls):
        return cls("REVIEW")
    
    @schemas.classproperty
    def VENDOR_ERROR(cls):
        return cls("VENDOR_ERROR")
    
    @schemas.classproperty
    def REJECTED(cls):
        return cls("REJECTED")
