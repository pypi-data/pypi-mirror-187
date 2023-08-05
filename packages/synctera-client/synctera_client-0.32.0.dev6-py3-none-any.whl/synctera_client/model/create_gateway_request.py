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


class CreateGatewayRequest(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "card_products",
            "url",
        }
        
        class properties:
            
            
            class card_products(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.UUIDSchema
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, uuid.UUID, ]], typing.List[typing.Union[MetaOapg.items, str, uuid.UUID, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'card_products':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            
            
            class url(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    format = 'uri'
                    max_length = 1000
            active = schemas.BoolSchema
        
            @staticmethod
            def custom_headers() -> typing.Type['GatewayCustomHeaders']:
                return GatewayCustomHeaders
            __annotations__ = {
                "card_products": card_products,
                "url": url,
                "active": active,
                "custom_headers": custom_headers,
            }
    
    card_products: MetaOapg.properties.card_products
    url: MetaOapg.properties.url
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["card_products"]) -> MetaOapg.properties.card_products: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["url"]) -> MetaOapg.properties.url: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["active"]) -> MetaOapg.properties.active: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["custom_headers"]) -> 'GatewayCustomHeaders': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["card_products", "url", "active", "custom_headers", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["card_products"]) -> MetaOapg.properties.card_products: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["url"]) -> MetaOapg.properties.url: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["active"]) -> typing.Union[MetaOapg.properties.active, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["custom_headers"]) -> typing.Union['GatewayCustomHeaders', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["card_products", "url", "active", "custom_headers", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        card_products: typing.Union[MetaOapg.properties.card_products, list, tuple, ],
        url: typing.Union[MetaOapg.properties.url, str, ],
        active: typing.Union[MetaOapg.properties.active, bool, schemas.Unset] = schemas.unset,
        custom_headers: typing.Union['GatewayCustomHeaders', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CreateGatewayRequest':
        return super().__new__(
            cls,
            *_args,
            card_products=card_products,
            url=url,
            active=active,
            custom_headers=custom_headers,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.gateway_custom_headers import GatewayCustomHeaders
