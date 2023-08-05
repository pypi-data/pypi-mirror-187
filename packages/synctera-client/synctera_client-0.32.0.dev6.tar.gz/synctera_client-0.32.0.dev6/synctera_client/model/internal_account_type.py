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


class InternalAccountType(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    type associated with the internal account.
    """


    class MetaOapg:
        enum_value_to_name = {
            "ACH_SETTLEMENT": "ACH_SETTLEMENT",
            "ACH_SUSPENSE": "ACH_SUSPENSE",
            "CARD_SETTLEMENT": "CARD_SETTLEMENT",
            "INTEREST_PAYOUT": "INTEREST_PAYOUT",
            "WIRE_SETTLEMENT": "WIRE_SETTLEMENT",
            "WIRE_SUSPENSE": "WIRE_SUSPENSE",
            "CHECK_SETTLEMENT": "CHECK_SETTLEMENT",
            "CASH_SETTLEMENT": "CASH_SETTLEMENT",
            "CASH_SUSPENSE": "CASH_SUSPENSE",
            "NETWORK_ADJUSTMENT": "NETWORK_ADJUSTMENT",
            "FEES": "FEES",
            "REWARDS": "REWARDS",
        }
    
    @schemas.classproperty
    def ACH_SETTLEMENT(cls):
        return cls("ACH_SETTLEMENT")
    
    @schemas.classproperty
    def ACH_SUSPENSE(cls):
        return cls("ACH_SUSPENSE")
    
    @schemas.classproperty
    def CARD_SETTLEMENT(cls):
        return cls("CARD_SETTLEMENT")
    
    @schemas.classproperty
    def INTEREST_PAYOUT(cls):
        return cls("INTEREST_PAYOUT")
    
    @schemas.classproperty
    def WIRE_SETTLEMENT(cls):
        return cls("WIRE_SETTLEMENT")
    
    @schemas.classproperty
    def WIRE_SUSPENSE(cls):
        return cls("WIRE_SUSPENSE")
    
    @schemas.classproperty
    def CHECK_SETTLEMENT(cls):
        return cls("CHECK_SETTLEMENT")
    
    @schemas.classproperty
    def CASH_SETTLEMENT(cls):
        return cls("CASH_SETTLEMENT")
    
    @schemas.classproperty
    def CASH_SUSPENSE(cls):
        return cls("CASH_SUSPENSE")
    
    @schemas.classproperty
    def NETWORK_ADJUSTMENT(cls):
        return cls("NETWORK_ADJUSTMENT")
    
    @schemas.classproperty
    def FEES(cls):
        return cls("FEES")
    
    @schemas.classproperty
    def REWARDS(cls):
        return cls("REWARDS")
