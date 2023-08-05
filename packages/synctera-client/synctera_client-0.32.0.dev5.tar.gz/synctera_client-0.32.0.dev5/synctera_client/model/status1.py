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


class Status1(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Status of the person. One of the following:
* `ACTIVE` – is an integrator defined status.  Integrators should set a person to active if they believe the person to be qualified for conducting business.  Synctera will combine this status with other statuses such a verification to determine if the person is eligible for specific actions such as initiating transactions or issuing a card.
* `DECEASED` – person is deceased.
* `DENIED` – customer was turned down.
* `DORMANT` – person is no longer active.
* `ESCHEAT` – person's assets are abandoned and are property of the state.
* `FROZEN` – person's actions are blocked for security, legal, or other reasons.
* `INACTIVE` – an inactive status indicating that the person is no longer active.
* `PROSPECT` – a potential customer, used for information-gathering and disclosures.
* `SANCTION` – person is on a sanctions list and should be carefully monitored.

    """


    class MetaOapg:
        enum_value_to_name = {
            "ACTIVE": "ACTIVE",
            "DECEASED": "DECEASED",
            "DENIED": "DENIED",
            "DORMANT": "DORMANT",
            "ESCHEAT": "ESCHEAT",
            "FROZEN": "FROZEN",
            "INACTIVE": "INACTIVE",
            "PROSPECT": "PROSPECT",
            "SANCTION": "SANCTION",
        }
    
    @schemas.classproperty
    def ACTIVE(cls):
        return cls("ACTIVE")
    
    @schemas.classproperty
    def DECEASED(cls):
        return cls("DECEASED")
    
    @schemas.classproperty
    def DENIED(cls):
        return cls("DENIED")
    
    @schemas.classproperty
    def DORMANT(cls):
        return cls("DORMANT")
    
    @schemas.classproperty
    def ESCHEAT(cls):
        return cls("ESCHEAT")
    
    @schemas.classproperty
    def FROZEN(cls):
        return cls("FROZEN")
    
    @schemas.classproperty
    def INACTIVE(cls):
        return cls("INACTIVE")
    
    @schemas.classproperty
    def PROSPECT(cls):
        return cls("PROSPECT")
    
    @schemas.classproperty
    def SANCTION(cls):
        return cls("SANCTION")
