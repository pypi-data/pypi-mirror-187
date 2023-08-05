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


class EventTypeExplicit(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    All the webhook event types
    """
    
    @schemas.classproperty
    def ACCOUNT_CREATED(cls):
        return cls("ACCOUNT.CREATED")
    
    @schemas.classproperty
    def ACCOUNT_UPDATED(cls):
        return cls("ACCOUNT.UPDATED")
    
    @schemas.classproperty
    def CARD_UPDATED(cls):
        return cls("CARD.UPDATED")
    
    @schemas.classproperty
    def CARD_IMAGE_UPDATED(cls):
        return cls("CARD.IMAGE.UPDATED")
    
    @schemas.classproperty
    def CASE_UPDATED(cls):
        return cls("CASE.UPDATED")
    
    @schemas.classproperty
    def CUSTOMER_UPDATED(cls):
        return cls("CUSTOMER.UPDATED")
    
    @schemas.classproperty
    def CUSTOMER_KYC_OUTCOME_UPDATED(cls):
        return cls("CUSTOMER.KYC_OUTCOME.UPDATED")
    
    @schemas.classproperty
    def BUSINESS_VERIFICATION_OUTCOME_UPDATED(cls):
        return cls("BUSINESS.VERIFICATION_OUTCOME.UPDATED")
    
    @schemas.classproperty
    def PERSON_VERIFICATION_OUTCOME_UPDATED(cls):
        return cls("PERSON.VERIFICATION_OUTCOME.UPDATED")
    
    @schemas.classproperty
    def INTEREST_MONTHLY_PAYOUT(cls):
        return cls("INTEREST.MONTHLY_PAYOUT")
    
    @schemas.classproperty
    def INTERNAL_TRANSFER_SUCCEEDED(cls):
        return cls("INTERNAL_TRANSFER.SUCCEEDED")
    
    @schemas.classproperty
    def TRANSACTION_POSTED_CREATED(cls):
        return cls("TRANSACTION.POSTED.CREATED")
    
    @schemas.classproperty
    def TRANSACTION_POSTED_UPDATED(cls):
        return cls("TRANSACTION.POSTED.UPDATED")
    
    @schemas.classproperty
    def TRANSACTION_PENDING_CREATED(cls):
        return cls("TRANSACTION.PENDING.CREATED")
    
    @schemas.classproperty
    def TRANSACTION_PENDING_UPDATED(cls):
        return cls("TRANSACTION.PENDING.UPDATED")
    
    @schemas.classproperty
    def CARD_DIGITALWALLETTOKEN_CREATED(cls):
        return cls("CARD.DIGITALWALLETTOKEN.CREATED")
    
    @schemas.classproperty
    def CARD_DIGITALWALLETTOKEN_UPDATED(cls):
        return cls("CARD.DIGITALWALLETTOKEN.UPDATED")
    
    @schemas.classproperty
    def PAYMENT_SCHEDULE_CREATED(cls):
        return cls("PAYMENT_SCHEDULE.CREATED")
    
    @schemas.classproperty
    def PAYMENT_SCHEDULE_UPDATED(cls):
        return cls("PAYMENT_SCHEDULE.UPDATED")
    
    @schemas.classproperty
    def PAYMENT_SCHEDULE_PAYMENT_CREATED(cls):
        return cls("PAYMENT_SCHEDULE.PAYMENT.CREATED")
    
    @schemas.classproperty
    def STATEMENT_CREATED(cls):
        return cls("STATEMENT.CREATED")
    
    @schemas.classproperty
    def EXTERNAL_CARD_CREATED(cls):
        return cls("EXTERNAL_CARD.CREATED")
    
    @schemas.classproperty
    def EXTERNAL_CARD_TRANSFER_CREATED(cls):
        return cls("EXTERNAL_CARD_TRANSFER.CREATED")
    
    @schemas.classproperty
    def APPLICATION_CREATED(cls):
        return cls("APPLICATION.CREATED")
    
    @schemas.classproperty
    def APPLICATION_UPDATED(cls):
        return cls("APPLICATION.UPDATED")
    
    @schemas.classproperty
    def CASH_PICKUP_CREATED(cls):
        return cls("CASH_PICKUP.CREATED")
    
    @schemas.classproperty
    def CASH_PICKUP_UPDATED(cls):
        return cls("CASH_PICKUP.UPDATED")
