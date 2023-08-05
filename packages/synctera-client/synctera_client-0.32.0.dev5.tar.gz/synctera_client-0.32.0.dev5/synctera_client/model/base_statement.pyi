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


class BaseStatement(
    schemas.ComposedBase,
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        
        
        class all_of_1(
            schemas.DictSchema
        ):
        
        
            class MetaOapg:
                
                class properties:
                
                    @staticmethod
                    def account_summary() -> typing.Type['AccountSummary']:
                        return AccountSummary
                    
                    
                    class authorized_signer(
                        schemas.ListSchema
                    ):
                    
                    
                        class MetaOapg:
                            
                            @staticmethod
                            def items() -> typing.Type['Person1']:
                                return Person1
                    
                        def __new__(
                            cls,
                            _arg: typing.Union[typing.Tuple['Person1'], typing.List['Person1']],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                        ) -> 'authorized_signer':
                            return super().__new__(
                                cls,
                                _arg,
                                _configuration=_configuration,
                            )
                    
                        def __getitem__(self, i: int) -> 'Person1':
                            return super().__getitem__(i)
                    disclosure = schemas.StrSchema
                    
                    
                    class joint_account_holders(
                        schemas.ListSchema
                    ):
                    
                    
                        class MetaOapg:
                            
                            @staticmethod
                            def items() -> typing.Type['Person1']:
                                return Person1
                    
                        def __new__(
                            cls,
                            _arg: typing.Union[typing.Tuple['Person1'], typing.List['Person1']],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                        ) -> 'joint_account_holders':
                            return super().__new__(
                                cls,
                                _arg,
                                _configuration=_configuration,
                            )
                    
                        def __getitem__(self, i: int) -> 'Person1':
                            return super().__getitem__(i)
                
                    @staticmethod
                    def primary_account_holder_business() -> typing.Type['Business1']:
                        return Business1
                
                    @staticmethod
                    def primary_account_holder_personal() -> typing.Type['Person1']:
                        return Person1
                    
                    
                    class transactions(
                        schemas.ListSchema
                    ):
                    
                    
                        class MetaOapg:
                            
                            @staticmethod
                            def items() -> typing.Type['Transaction']:
                                return Transaction
                    
                        def __new__(
                            cls,
                            _arg: typing.Union[typing.Tuple['Transaction'], typing.List['Transaction']],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                        ) -> 'transactions':
                            return super().__new__(
                                cls,
                                _arg,
                                _configuration=_configuration,
                            )
                    
                        def __getitem__(self, i: int) -> 'Transaction':
                            return super().__getitem__(i)
                    __annotations__ = {
                        "account_summary": account_summary,
                        "authorized_signer": authorized_signer,
                        "disclosure": disclosure,
                        "joint_account_holders": joint_account_holders,
                        "primary_account_holder_business": primary_account_holder_business,
                        "primary_account_holder_personal": primary_account_holder_personal,
                        "transactions": transactions,
                    }
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["account_summary"]) -> 'AccountSummary': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["authorized_signer"]) -> MetaOapg.properties.authorized_signer: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["disclosure"]) -> MetaOapg.properties.disclosure: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["joint_account_holders"]) -> MetaOapg.properties.joint_account_holders: ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["primary_account_holder_business"]) -> 'Business1': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["primary_account_holder_personal"]) -> 'Person1': ...
            
            @typing.overload
            def __getitem__(self, name: typing_extensions.Literal["transactions"]) -> MetaOapg.properties.transactions: ...
            
            @typing.overload
            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
            
            def __getitem__(self, name: typing.Union[typing_extensions.Literal["account_summary", "authorized_signer", "disclosure", "joint_account_holders", "primary_account_holder_business", "primary_account_holder_personal", "transactions", ], str]):
                # dict_instance[name] accessor
                return super().__getitem__(name)
            
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["account_summary"]) -> typing.Union['AccountSummary', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["authorized_signer"]) -> typing.Union[MetaOapg.properties.authorized_signer, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["disclosure"]) -> typing.Union[MetaOapg.properties.disclosure, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["joint_account_holders"]) -> typing.Union[MetaOapg.properties.joint_account_holders, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["primary_account_holder_business"]) -> typing.Union['Business1', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["primary_account_holder_personal"]) -> typing.Union['Person1', schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: typing_extensions.Literal["transactions"]) -> typing.Union[MetaOapg.properties.transactions, schemas.Unset]: ...
            
            @typing.overload
            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
            
            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["account_summary", "authorized_signer", "disclosure", "joint_account_holders", "primary_account_holder_business", "primary_account_holder_personal", "transactions", ], str]):
                return super().get_item_oapg(name)
            
        
            def __new__(
                cls,
                *_args: typing.Union[dict, frozendict.frozendict, ],
                account_summary: typing.Union['AccountSummary', schemas.Unset] = schemas.unset,
                authorized_signer: typing.Union[MetaOapg.properties.authorized_signer, list, tuple, schemas.Unset] = schemas.unset,
                disclosure: typing.Union[MetaOapg.properties.disclosure, str, schemas.Unset] = schemas.unset,
                joint_account_holders: typing.Union[MetaOapg.properties.joint_account_holders, list, tuple, schemas.Unset] = schemas.unset,
                primary_account_holder_business: typing.Union['Business1', schemas.Unset] = schemas.unset,
                primary_account_holder_personal: typing.Union['Person1', schemas.Unset] = schemas.unset,
                transactions: typing.Union[MetaOapg.properties.transactions, list, tuple, schemas.Unset] = schemas.unset,
                _configuration: typing.Optional[schemas.Configuration] = None,
                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
            ) -> 'all_of_1':
                return super().__new__(
                    cls,
                    *_args,
                    account_summary=account_summary,
                    authorized_signer=authorized_signer,
                    disclosure=disclosure,
                    joint_account_holders=joint_account_holders,
                    primary_account_holder_business=primary_account_holder_business,
                    primary_account_holder_personal=primary_account_holder_personal,
                    transactions=transactions,
                    _configuration=_configuration,
                    **kwargs,
                )
        
        @classmethod
        @functools.lru_cache()
        def all_of(cls):
            # we need this here to make our import statements work
            # we must store _composed_schemas in here so the code is only run
            # when we invoke this method. If we kept this at the class
            # level we would get an error because the class level
            # code would be run when this module is imported, and these composed
            # classes don't exist yet because their module has not finished
            # loading
            return [
                StatementSummary,
                cls.all_of_1,
            ]


    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'BaseStatement':
        return super().__new__(
            cls,
            *_args,
            _configuration=_configuration,
            **kwargs,
        )

from synctera_client.model.account_summary import AccountSummary
from synctera_client.model.business1 import Business1
from synctera_client.model.person1 import Person1
from synctera_client.model.statement_summary import StatementSummary
from synctera_client.model.transaction import Transaction
