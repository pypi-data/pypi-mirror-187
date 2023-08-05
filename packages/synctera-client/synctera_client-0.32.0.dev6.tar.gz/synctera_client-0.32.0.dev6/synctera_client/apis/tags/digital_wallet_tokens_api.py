# coding: utf-8

"""
    Synctera API

    <h2>Let's build something great.</h2><p>Welcome to the official reference documentation for Synctera APIs. Our APIs are the best way to automate your company's banking needs and are designed to be easy to understand and implement.</p><p>We're continuously growing this library and what you see here is just the start, but if you need something specific or have a question, <a class='text-blue-600' href='https://synctera.com/contact' target='_blank' rel='noreferrer'>contact us</a>.</p>   # noqa: E501

    The version of the OpenAPI document: 0.32.0.dev6
    Generated by: https://openapi-generator.tech
"""

from synctera_client.paths.cards_card_id_digital_wallet_tokens_applepay.post import CreateDigitalWalletApple
from synctera_client.paths.cards_card_id_digital_wallet_tokens_googlepay.post import CreateDigitalWalletGoogle
from synctera_client.paths.cards_digital_wallet_tokens_digital_wallet_token_id.get import GetDigitalWalletToken
from synctera_client.paths.cards_digital_wallet_tokens.get import ListDigitalWalletTokens
from synctera_client.paths.cards_digital_wallet_tokens_digital_wallet_token_id.patch import UpdateDigitalWalletTokenStatus


class DigitalWalletTokensApi(
    CreateDigitalWalletApple,
    CreateDigitalWalletGoogle,
    GetDigitalWalletToken,
    ListDigitalWalletTokens,
    UpdateDigitalWalletTokenStatus,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
