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


class PatchRelationshipIn(
    schemas.ComposedBase,
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        @staticmethod
        def discriminator():
            return {
                'relationship_type': {
                    'BENEFICIAL_OWNER_OF': PatchPersonBusinessOwnerRelationship,
                    'MANAGING_PERSON_OF': PatchPersonBusinessRelationship,
                    'OWNER_OF': PatchBusinessBusinessOwnerRelationship,
                    'patch_business_business_owner_relationship': PatchBusinessBusinessOwnerRelationship,
                    'patch_person_business_owner_relationship': PatchPersonBusinessOwnerRelationship,
                    'patch_person_business_relationship': PatchPersonBusinessRelationship,
                }
            }
        
        @classmethod
        @functools.lru_cache()
        def one_of(cls):
            # we need this here to make our import statements work
            # we must store _composed_schemas in here so the code is only run
            # when we invoke this method. If we kept this at the class
            # level we would get an error because the class level
            # code would be run when this module is imported, and these composed
            # classes don't exist yet because their module has not finished
            # loading
            return [
                PatchPersonBusinessRelationship,
                PatchPersonBusinessOwnerRelationship,
                PatchBusinessBusinessOwnerRelationship,
            ]


    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'PatchRelationshipIn':
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.patch_business_business_owner_relationship import PatchBusinessBusinessOwnerRelationship
from synctera_client.model.patch_person_business_owner_relationship import PatchPersonBusinessOwnerRelationship
from synctera_client.model.patch_person_business_relationship import PatchPersonBusinessRelationship
