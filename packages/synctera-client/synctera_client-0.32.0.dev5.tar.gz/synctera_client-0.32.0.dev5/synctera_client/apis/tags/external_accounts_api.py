# coding: utf-8

"""
    Synctera API

    <h2>Let's build something great.</h2><p>Welcome to the official reference documentation for Synctera APIs. Our APIs are the best way to automate your company's banking needs and are designed to be easy to understand and implement.</p><p>We're continuously growing this library and what you see here is just the start, but if you need something specific or have a question, <a class='text-blue-600' href='https://synctera.com/contact' target='_blank' rel='noreferrer'>contact us</a>.</p>   # noqa: E501

    The version of the OpenAPI document: 0.32.0.dev5
    Generated by: https://openapi-generator.tech
"""

from synctera_client.paths.external_accounts.post import AddExternalAccounts
from synctera_client.paths.external_accounts_add_vendor_accounts.post import AddVendorExternalAccounts
from synctera_client.paths.external_accounts_access_tokens.post import CreateAccessToken
from synctera_client.paths.external_accounts_link_tokens.post import CreateVerificationLinkToken
from synctera_client.paths.external_accounts_external_account_id.delete import DeleteExternalAccount
from synctera_client.paths.external_accounts_external_account_id.get import GetExternalAccount
from synctera_client.paths.external_accounts_external_account_id_balance.get import GetExternalAccountBalance
from synctera_client.paths.external_accounts_external_account_id_transactions.get import GetExternalAccountTransactions
from synctera_client.paths.external_accounts.get import ListExternalAccounts
from synctera_client.paths.external_accounts_sync_vendor_accounts.post import SyncVendorExternalAccounts
from synctera_client.paths.external_accounts_external_account_id.patch import UpdateExternalAccount


class ExternalAccountsApi(
    AddExternalAccounts,
    AddVendorExternalAccounts,
    CreateAccessToken,
    CreateVerificationLinkToken,
    DeleteExternalAccount,
    GetExternalAccount,
    GetExternalAccountBalance,
    GetExternalAccountTransactions,
    ListExternalAccounts,
    SyncVendorExternalAccounts,
    UpdateExternalAccount,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
