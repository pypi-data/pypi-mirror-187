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


class TransactionData(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "memo",
            "lines",
        }
        
        class properties:
            
            
            class lines(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['TransactionLine']:
                        return TransactionLine
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple['TransactionLine'], typing.List['TransactionLine']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'lines':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'TransactionLine':
                    return super().__getitem__(i)
            memo = schemas.StrSchema
            
            
            class external_data(
                schemas.DictBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneFrozenDictMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'external_data':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class metadata(
                schemas.DictBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneFrozenDictMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'metadata':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            __annotations__ = {
                "lines": lines,
                "memo": memo,
                "external_data": external_data,
                "metadata": metadata,
            }
    
    memo: MetaOapg.properties.memo
    lines: MetaOapg.properties.lines
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["lines"]) -> MetaOapg.properties.lines: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["memo"]) -> MetaOapg.properties.memo: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["external_data"]) -> MetaOapg.properties.external_data: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["lines", "memo", "external_data", "metadata", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["lines"]) -> MetaOapg.properties.lines: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["memo"]) -> MetaOapg.properties.memo: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["external_data"]) -> typing.Union[MetaOapg.properties.external_data, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["lines", "memo", "external_data", "metadata", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        memo: typing.Union[MetaOapg.properties.memo, str, ],
        lines: typing.Union[MetaOapg.properties.lines, list, tuple, ],
        external_data: typing.Union[MetaOapg.properties.external_data, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'TransactionData':
        return super().__new__(
            cls,
            *_args,
            memo=memo,
            lines=lines,
            external_data=external_data,
            metadata=metadata,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.transaction_line import TransactionLine
