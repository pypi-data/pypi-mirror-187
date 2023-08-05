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


class AchTransactionSubtypes(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    The set of valid ACH transaction subtypes
    """
    
    @schemas.classproperty
    def INCOMING_CREDIT(cls):
        return cls("INCOMING_CREDIT")
    
    @schemas.classproperty
    def INCOMING_CREDIT_CONTESTED_RETURN(cls):
        return cls("INCOMING_CREDIT_CONTESTED_RETURN")
    
    @schemas.classproperty
    def INCOMING_CREDIT_DISHONORED_RETURN(cls):
        return cls("INCOMING_CREDIT_DISHONORED_RETURN")
    
    @schemas.classproperty
    def INCOMING_CREDIT_RETURN(cls):
        return cls("INCOMING_CREDIT_RETURN")
    
    @schemas.classproperty
    def INCOMING_CREDIT_REVERSAL(cls):
        return cls("INCOMING_CREDIT_REVERSAL")
    
    @schemas.classproperty
    def INCOMING_DEBIT(cls):
        return cls("INCOMING_DEBIT")
    
    @schemas.classproperty
    def INCOMING_DEBIT_CONTESTED_RETURN(cls):
        return cls("INCOMING_DEBIT_CONTESTED_RETURN")
    
    @schemas.classproperty
    def INCOMING_DEBIT_DISHONORED_RETURN(cls):
        return cls("INCOMING_DEBIT_DISHONORED_RETURN")
    
    @schemas.classproperty
    def INCOMING_DEBIT_DISHONORED_RETURN_REVERSAL(cls):
        return cls("INCOMING_DEBIT_DISHONORED_RETURN_REVERSAL")
    
    @schemas.classproperty
    def INCOMING_DEBIT_RETURN(cls):
        return cls("INCOMING_DEBIT_RETURN")
    
    @schemas.classproperty
    def INCOMING_DEBIT_RETURN_REVERSAL(cls):
        return cls("INCOMING_DEBIT_RETURN_REVERSAL")
    
    @schemas.classproperty
    def INCOMING_DEBIT_REVERSAL(cls):
        return cls("INCOMING_DEBIT_REVERSAL")
    
    @schemas.classproperty
    def OUTGOING_CREDIT(cls):
        return cls("OUTGOING_CREDIT")
    
    @schemas.classproperty
    def OUTGOING_CREDIT_CONTESTED_RETURN(cls):
        return cls("OUTGOING_CREDIT_CONTESTED_RETURN")
    
    @schemas.classproperty
    def OUTGOING_CREDIT_DISHONORED_RETURN(cls):
        return cls("OUTGOING_CREDIT_DISHONORED_RETURN")
    
    @schemas.classproperty
    def OUTGOING_CREDIT_RETURN(cls):
        return cls("OUTGOING_CREDIT_RETURN")
    
    @schemas.classproperty
    def OUTGOING_CREDIT_REVERSAL(cls):
        return cls("OUTGOING_CREDIT_REVERSAL")
    
    @schemas.classproperty
    def OUTGOING_DEBIT(cls):
        return cls("OUTGOING_DEBIT")
    
    @schemas.classproperty
    def OUTGOING_DEBIT_CONTESTED_RETURN(cls):
        return cls("OUTGOING_DEBIT_CONTESTED_RETURN")
    
    @schemas.classproperty
    def OUTGOING_DEBIT_DISHONORED_RETURN(cls):
        return cls("OUTGOING_DEBIT_DISHONORED_RETURN")
    
    @schemas.classproperty
    def OUTGOING_DEBIT_RETURN(cls):
        return cls("OUTGOING_DEBIT_RETURN")
    
    @schemas.classproperty
    def OUTGOING_DEBIT_REVERSAL(cls):
        return cls("OUTGOING_DEBIT_REVERSAL")
    
    @schemas.classproperty
    def PRENOTE(cls):
        return cls("PRENOTE")
    
    @schemas.classproperty
    def TEMP_HOLD(cls):
        return cls("TEMP_HOLD")
