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


class GoogleDigitalWalletProvisionRequest(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "device_id",
            "wallet_account_id",
            "device_type",
            "provisioning_app_version",
        }
        
        class properties:
            
            
            class device_id(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 24
        
            @staticmethod
            def device_type() -> typing.Type['DeviceType']:
                return DeviceType
        
            @staticmethod
            def provisioning_app_version() -> typing.Type['ProvisioningAppVersion']:
                return ProvisioningAppVersion
            
            
            class wallet_account_id(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    max_length = 50
            __annotations__ = {
                "device_id": device_id,
                "device_type": device_type,
                "provisioning_app_version": provisioning_app_version,
                "wallet_account_id": wallet_account_id,
            }
    
    device_id: MetaOapg.properties.device_id
    wallet_account_id: MetaOapg.properties.wallet_account_id
    device_type: 'DeviceType'
    provisioning_app_version: 'ProvisioningAppVersion'
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["device_id"]) -> MetaOapg.properties.device_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["device_type"]) -> 'DeviceType': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["provisioning_app_version"]) -> 'ProvisioningAppVersion': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["wallet_account_id"]) -> MetaOapg.properties.wallet_account_id: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["device_id", "device_type", "provisioning_app_version", "wallet_account_id", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["device_id"]) -> MetaOapg.properties.device_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["device_type"]) -> 'DeviceType': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["provisioning_app_version"]) -> 'ProvisioningAppVersion': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["wallet_account_id"]) -> MetaOapg.properties.wallet_account_id: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["device_id", "device_type", "provisioning_app_version", "wallet_account_id", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        device_id: typing.Union[MetaOapg.properties.device_id, str, ],
        wallet_account_id: typing.Union[MetaOapg.properties.wallet_account_id, str, ],
        device_type: 'DeviceType',
        provisioning_app_version: 'ProvisioningAppVersion',
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'GoogleDigitalWalletProvisionRequest':
        return super().__new__(
            cls,
            *_args,
            device_id=device_id,
            wallet_account_id=wallet_account_id,
            device_type=device_type,
            provisioning_app_version=provisioning_app_version,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.device_type import DeviceType
from synctera_client.model.provisioning_app_version import ProvisioningAppVersion
