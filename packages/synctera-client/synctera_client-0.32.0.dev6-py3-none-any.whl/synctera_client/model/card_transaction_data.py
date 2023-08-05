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


class CardTransactionData(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Transaction metadata specific to transactions with type `CARD`
    """


    class MetaOapg:
        
        class properties:
            card_id = schemas.UUIDSchema
            currency_code = schemas.StrSchema
            
            
            class currency_conversion(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        conversion_rate = schemas.NumberSchema
                        original_amount = schemas.IntSchema
                        original_currency_code = schemas.StrSchema
                        __annotations__ = {
                            "conversion_rate": conversion_rate,
                            "original_amount": original_amount,
                            "original_currency_code": original_currency_code,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["conversion_rate"]) -> MetaOapg.properties.conversion_rate: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["original_amount"]) -> MetaOapg.properties.original_amount: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["original_currency_code"]) -> MetaOapg.properties.original_currency_code: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["conversion_rate", "original_amount", "original_currency_code", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["conversion_rate"]) -> typing.Union[MetaOapg.properties.conversion_rate, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["original_amount"]) -> typing.Union[MetaOapg.properties.original_amount, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["original_currency_code"]) -> typing.Union[MetaOapg.properties.original_currency_code, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["conversion_rate", "original_amount", "original_currency_code", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    conversion_rate: typing.Union[MetaOapg.properties.conversion_rate, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
                    original_amount: typing.Union[MetaOapg.properties.original_amount, decimal.Decimal, int, schemas.Unset] = schemas.unset,
                    original_currency_code: typing.Union[MetaOapg.properties.original_currency_code, str, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'currency_conversion':
                    return super().__new__(
                        cls,
                        *_args,
                        conversion_rate=conversion_rate,
                        original_amount=original_amount,
                        original_currency_code=original_currency_code,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class merchant(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        address = schemas.StrSchema
                        city = schemas.StrSchema
                        country_code = schemas.StrSchema
                        independent_sales_organization_id = schemas.StrSchema
                        mcc = schemas.StrSchema
                        mid = schemas.StrSchema
                        name = schemas.StrSchema
                        payment_facilitator_id = schemas.StrSchema
                        postal_code = schemas.StrSchema
                        state = schemas.StrSchema
                        sub_merchant_id = schemas.StrSchema
                        __annotations__ = {
                            "address": address,
                            "city": city,
                            "country_code": country_code,
                            "independent_sales_organization_id": independent_sales_organization_id,
                            "mcc": mcc,
                            "mid": mid,
                            "name": name,
                            "payment_facilitator_id": payment_facilitator_id,
                            "postal_code": postal_code,
                            "state": state,
                            "sub_merchant_id": sub_merchant_id,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["address"]) -> MetaOapg.properties.address: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["city"]) -> MetaOapg.properties.city: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["country_code"]) -> MetaOapg.properties.country_code: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["independent_sales_organization_id"]) -> MetaOapg.properties.independent_sales_organization_id: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["mcc"]) -> MetaOapg.properties.mcc: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["mid"]) -> MetaOapg.properties.mid: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["payment_facilitator_id"]) -> MetaOapg.properties.payment_facilitator_id: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["postal_code"]) -> MetaOapg.properties.postal_code: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["state"]) -> MetaOapg.properties.state: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["sub_merchant_id"]) -> MetaOapg.properties.sub_merchant_id: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["address", "city", "country_code", "independent_sales_organization_id", "mcc", "mid", "name", "payment_facilitator_id", "postal_code", "state", "sub_merchant_id", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["address"]) -> typing.Union[MetaOapg.properties.address, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["city"]) -> typing.Union[MetaOapg.properties.city, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["country_code"]) -> typing.Union[MetaOapg.properties.country_code, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["independent_sales_organization_id"]) -> typing.Union[MetaOapg.properties.independent_sales_organization_id, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["mcc"]) -> typing.Union[MetaOapg.properties.mcc, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["mid"]) -> typing.Union[MetaOapg.properties.mid, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["payment_facilitator_id"]) -> typing.Union[MetaOapg.properties.payment_facilitator_id, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["postal_code"]) -> typing.Union[MetaOapg.properties.postal_code, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["state"]) -> typing.Union[MetaOapg.properties.state, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["sub_merchant_id"]) -> typing.Union[MetaOapg.properties.sub_merchant_id, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["address", "city", "country_code", "independent_sales_organization_id", "mcc", "mid", "name", "payment_facilitator_id", "postal_code", "state", "sub_merchant_id", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    address: typing.Union[MetaOapg.properties.address, str, schemas.Unset] = schemas.unset,
                    city: typing.Union[MetaOapg.properties.city, str, schemas.Unset] = schemas.unset,
                    country_code: typing.Union[MetaOapg.properties.country_code, str, schemas.Unset] = schemas.unset,
                    independent_sales_organization_id: typing.Union[MetaOapg.properties.independent_sales_organization_id, str, schemas.Unset] = schemas.unset,
                    mcc: typing.Union[MetaOapg.properties.mcc, str, schemas.Unset] = schemas.unset,
                    mid: typing.Union[MetaOapg.properties.mid, str, schemas.Unset] = schemas.unset,
                    name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
                    payment_facilitator_id: typing.Union[MetaOapg.properties.payment_facilitator_id, str, schemas.Unset] = schemas.unset,
                    postal_code: typing.Union[MetaOapg.properties.postal_code, str, schemas.Unset] = schemas.unset,
                    state: typing.Union[MetaOapg.properties.state, str, schemas.Unset] = schemas.unset,
                    sub_merchant_id: typing.Union[MetaOapg.properties.sub_merchant_id, str, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'merchant':
                    return super().__new__(
                        cls,
                        *_args,
                        address=address,
                        city=city,
                        country_code=country_code,
                        independent_sales_organization_id=independent_sales_organization_id,
                        mcc=mcc,
                        mid=mid,
                        name=name,
                        payment_facilitator_id=payment_facilitator_id,
                        postal_code=postal_code,
                        state=state,
                        sub_merchant_id=sub_merchant_id,
                        _configuration=_configuration,
                        **kwargs,
                    )
            network = schemas.StrSchema
            network_reference_id = schemas.StrSchema
            
            
            class pos(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        card_data_input_capability = schemas.StrSchema
                        card_holder_presence = schemas.BoolSchema
                        card_presence = schemas.BoolSchema
                        cardholder_authentication_method = schemas.StrSchema
                        country_code = schemas.StrSchema
                        is_installment = schemas.BoolSchema
                        is_recurring = schemas.BoolSchema
                        pan_entry_mode = schemas.StrSchema
                        partial_approval_capable = schemas.BoolSchema
                        pin_entry_mode = schemas.StrSchema
                        pin_present = schemas.BoolSchema
                        purchase_amount_only = schemas.BoolSchema
                        terminal_attendance = schemas.StrSchema
                        terminal_id = schemas.StrSchema
                        terminal_location = schemas.StrSchema
                        terminal_type = schemas.StrSchema
                        zip = schemas.StrSchema
                        __annotations__ = {
                            "card_data_input_capability": card_data_input_capability,
                            "card_holder_presence": card_holder_presence,
                            "card_presence": card_presence,
                            "cardholder_authentication_method": cardholder_authentication_method,
                            "country_code": country_code,
                            "is_installment": is_installment,
                            "is_recurring": is_recurring,
                            "pan_entry_mode": pan_entry_mode,
                            "partial_approval_capable": partial_approval_capable,
                            "pin_entry_mode": pin_entry_mode,
                            "pin_present": pin_present,
                            "purchase_amount_only": purchase_amount_only,
                            "terminal_attendance": terminal_attendance,
                            "terminal_id": terminal_id,
                            "terminal_location": terminal_location,
                            "terminal_type": terminal_type,
                            "zip": zip,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["card_data_input_capability"]) -> MetaOapg.properties.card_data_input_capability: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["card_holder_presence"]) -> MetaOapg.properties.card_holder_presence: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["card_presence"]) -> MetaOapg.properties.card_presence: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["cardholder_authentication_method"]) -> MetaOapg.properties.cardholder_authentication_method: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["country_code"]) -> MetaOapg.properties.country_code: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["is_installment"]) -> MetaOapg.properties.is_installment: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["is_recurring"]) -> MetaOapg.properties.is_recurring: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["pan_entry_mode"]) -> MetaOapg.properties.pan_entry_mode: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["partial_approval_capable"]) -> MetaOapg.properties.partial_approval_capable: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["pin_entry_mode"]) -> MetaOapg.properties.pin_entry_mode: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["pin_present"]) -> MetaOapg.properties.pin_present: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["purchase_amount_only"]) -> MetaOapg.properties.purchase_amount_only: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["terminal_attendance"]) -> MetaOapg.properties.terminal_attendance: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["terminal_id"]) -> MetaOapg.properties.terminal_id: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["terminal_location"]) -> MetaOapg.properties.terminal_location: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["terminal_type"]) -> MetaOapg.properties.terminal_type: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["zip"]) -> MetaOapg.properties.zip: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["card_data_input_capability", "card_holder_presence", "card_presence", "cardholder_authentication_method", "country_code", "is_installment", "is_recurring", "pan_entry_mode", "partial_approval_capable", "pin_entry_mode", "pin_present", "purchase_amount_only", "terminal_attendance", "terminal_id", "terminal_location", "terminal_type", "zip", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["card_data_input_capability"]) -> typing.Union[MetaOapg.properties.card_data_input_capability, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["card_holder_presence"]) -> typing.Union[MetaOapg.properties.card_holder_presence, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["card_presence"]) -> typing.Union[MetaOapg.properties.card_presence, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["cardholder_authentication_method"]) -> typing.Union[MetaOapg.properties.cardholder_authentication_method, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["country_code"]) -> typing.Union[MetaOapg.properties.country_code, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["is_installment"]) -> typing.Union[MetaOapg.properties.is_installment, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["is_recurring"]) -> typing.Union[MetaOapg.properties.is_recurring, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["pan_entry_mode"]) -> typing.Union[MetaOapg.properties.pan_entry_mode, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["partial_approval_capable"]) -> typing.Union[MetaOapg.properties.partial_approval_capable, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["pin_entry_mode"]) -> typing.Union[MetaOapg.properties.pin_entry_mode, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["pin_present"]) -> typing.Union[MetaOapg.properties.pin_present, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["purchase_amount_only"]) -> typing.Union[MetaOapg.properties.purchase_amount_only, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["terminal_attendance"]) -> typing.Union[MetaOapg.properties.terminal_attendance, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["terminal_id"]) -> typing.Union[MetaOapg.properties.terminal_id, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["terminal_location"]) -> typing.Union[MetaOapg.properties.terminal_location, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["terminal_type"]) -> typing.Union[MetaOapg.properties.terminal_type, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["zip"]) -> typing.Union[MetaOapg.properties.zip, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["card_data_input_capability", "card_holder_presence", "card_presence", "cardholder_authentication_method", "country_code", "is_installment", "is_recurring", "pan_entry_mode", "partial_approval_capable", "pin_entry_mode", "pin_present", "purchase_amount_only", "terminal_attendance", "terminal_id", "terminal_location", "terminal_type", "zip", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    card_data_input_capability: typing.Union[MetaOapg.properties.card_data_input_capability, str, schemas.Unset] = schemas.unset,
                    card_holder_presence: typing.Union[MetaOapg.properties.card_holder_presence, bool, schemas.Unset] = schemas.unset,
                    card_presence: typing.Union[MetaOapg.properties.card_presence, bool, schemas.Unset] = schemas.unset,
                    cardholder_authentication_method: typing.Union[MetaOapg.properties.cardholder_authentication_method, str, schemas.Unset] = schemas.unset,
                    country_code: typing.Union[MetaOapg.properties.country_code, str, schemas.Unset] = schemas.unset,
                    is_installment: typing.Union[MetaOapg.properties.is_installment, bool, schemas.Unset] = schemas.unset,
                    is_recurring: typing.Union[MetaOapg.properties.is_recurring, bool, schemas.Unset] = schemas.unset,
                    pan_entry_mode: typing.Union[MetaOapg.properties.pan_entry_mode, str, schemas.Unset] = schemas.unset,
                    partial_approval_capable: typing.Union[MetaOapg.properties.partial_approval_capable, bool, schemas.Unset] = schemas.unset,
                    pin_entry_mode: typing.Union[MetaOapg.properties.pin_entry_mode, str, schemas.Unset] = schemas.unset,
                    pin_present: typing.Union[MetaOapg.properties.pin_present, bool, schemas.Unset] = schemas.unset,
                    purchase_amount_only: typing.Union[MetaOapg.properties.purchase_amount_only, bool, schemas.Unset] = schemas.unset,
                    terminal_attendance: typing.Union[MetaOapg.properties.terminal_attendance, str, schemas.Unset] = schemas.unset,
                    terminal_id: typing.Union[MetaOapg.properties.terminal_id, str, schemas.Unset] = schemas.unset,
                    terminal_location: typing.Union[MetaOapg.properties.terminal_location, str, schemas.Unset] = schemas.unset,
                    terminal_type: typing.Union[MetaOapg.properties.terminal_type, str, schemas.Unset] = schemas.unset,
                    zip: typing.Union[MetaOapg.properties.zip, str, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'pos':
                    return super().__new__(
                        cls,
                        *_args,
                        card_data_input_capability=card_data_input_capability,
                        card_holder_presence=card_holder_presence,
                        card_presence=card_presence,
                        cardholder_authentication_method=cardholder_authentication_method,
                        country_code=country_code,
                        is_installment=is_installment,
                        is_recurring=is_recurring,
                        pan_entry_mode=pan_entry_mode,
                        partial_approval_capable=partial_approval_capable,
                        pin_entry_mode=pin_entry_mode,
                        pin_present=pin_present,
                        purchase_amount_only=purchase_amount_only,
                        terminal_attendance=terminal_attendance,
                        terminal_id=terminal_id,
                        terminal_location=terminal_location,
                        terminal_type=terminal_type,
                        zip=zip,
                        _configuration=_configuration,
                        **kwargs,
                    )
            __annotations__ = {
                "card_id": card_id,
                "currency_code": currency_code,
                "currency_conversion": currency_conversion,
                "merchant": merchant,
                "network": network,
                "network_reference_id": network_reference_id,
                "pos": pos,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["card_id"]) -> MetaOapg.properties.card_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["currency_code"]) -> MetaOapg.properties.currency_code: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["currency_conversion"]) -> MetaOapg.properties.currency_conversion: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["merchant"]) -> MetaOapg.properties.merchant: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["network"]) -> MetaOapg.properties.network: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["network_reference_id"]) -> MetaOapg.properties.network_reference_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["pos"]) -> MetaOapg.properties.pos: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["card_id", "currency_code", "currency_conversion", "merchant", "network", "network_reference_id", "pos", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["card_id"]) -> typing.Union[MetaOapg.properties.card_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["currency_code"]) -> typing.Union[MetaOapg.properties.currency_code, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["currency_conversion"]) -> typing.Union[MetaOapg.properties.currency_conversion, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["merchant"]) -> typing.Union[MetaOapg.properties.merchant, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["network"]) -> typing.Union[MetaOapg.properties.network, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["network_reference_id"]) -> typing.Union[MetaOapg.properties.network_reference_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["pos"]) -> typing.Union[MetaOapg.properties.pos, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["card_id", "currency_code", "currency_conversion", "merchant", "network", "network_reference_id", "pos", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        card_id: typing.Union[MetaOapg.properties.card_id, str, uuid.UUID, schemas.Unset] = schemas.unset,
        currency_code: typing.Union[MetaOapg.properties.currency_code, str, schemas.Unset] = schemas.unset,
        currency_conversion: typing.Union[MetaOapg.properties.currency_conversion, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        merchant: typing.Union[MetaOapg.properties.merchant, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        network: typing.Union[MetaOapg.properties.network, str, schemas.Unset] = schemas.unset,
        network_reference_id: typing.Union[MetaOapg.properties.network_reference_id, str, schemas.Unset] = schemas.unset,
        pos: typing.Union[MetaOapg.properties.pos, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'CardTransactionData':
        return super().__new__(
            cls,
            *_args,
            card_id=card_id,
            currency_code=currency_code,
            currency_conversion=currency_conversion,
            merchant=merchant,
            network=network,
            network_reference_id=network_reference_id,
            pos=pos,
            _configuration=_configuration,
            **kwargs,
        )
