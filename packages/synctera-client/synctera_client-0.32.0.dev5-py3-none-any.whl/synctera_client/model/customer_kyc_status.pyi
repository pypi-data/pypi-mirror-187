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


class CustomerKycStatus(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Customer's KYC status
    """
    
    @schemas.classproperty
    def UNVERIFIED(cls):
        return cls("UNVERIFIED")
    
    @schemas.classproperty
    def REVIEW(cls):
        return cls("REVIEW")
    
    @schemas.classproperty
    def PROVIDER_FAILURE(cls):
        return cls("PROVIDER_FAILURE")
    
    @schemas.classproperty
    def ACCEPTED(cls):
        return cls("ACCEPTED")
    
    @schemas.classproperty
    def REJECTED(cls):
        return cls("REJECTED")
    
    @schemas.classproperty
    def PROVISIONAL(cls):
        return cls("PROVISIONAL")
