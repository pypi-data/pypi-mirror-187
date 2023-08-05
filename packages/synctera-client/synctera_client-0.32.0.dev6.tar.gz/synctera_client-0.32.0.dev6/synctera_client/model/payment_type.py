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


class PaymentType(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    The type of payment to which a spend control applies.
If this is not set, the spend control applies to all spending, regardless of payment type.

    """


    class MetaOapg:
        enum_value_to_name = {
            "CARD": "CARD",
            "ACH": "ACH",
            "CHECK": "CHECK",
            "INTERNAL_TRANSFER": "INTERNAL_TRANSFER",
            "WIRE": "WIRE",
            "CASH": "CASH",
            "EXTERNAL_CARD": "EXTERNAL_CARD",
        }
    
    @schemas.classproperty
    def CARD(cls):
        return cls("CARD")
    
    @schemas.classproperty
    def ACH(cls):
        return cls("ACH")
    
    @schemas.classproperty
    def CHECK(cls):
        return cls("CHECK")
    
    @schemas.classproperty
    def INTERNAL_TRANSFER(cls):
        return cls("INTERNAL_TRANSFER")
    
    @schemas.classproperty
    def WIRE(cls):
        return cls("WIRE")
    
    @schemas.classproperty
    def CASH(cls):
        return cls("CASH")
    
    @schemas.classproperty
    def EXTERNAL_CARD(cls):
        return cls("EXTERNAL_CARD")
