# coding: utf-8

"""
    Synctera API

    <h2>Let's build something great.</h2><p>Welcome to the official reference documentation for Synctera APIs. Our APIs are the best way to automate your company's banking needs and are designed to be easy to understand and implement.</p><p>We're continuously growing this library and what you see here is just the start, but if you need something specific or have a question, <a class='text-blue-600' href='https://synctera.com/contact' target='_blank' rel='noreferrer'>contact us</a>.</p>   # noqa: E501

    The version of the OpenAPI document: 0.32.0.dev5
    Generated by: https://openapi-generator.tech
"""

from synctera_client.paths.documents.post import CreateDocument
from synctera_client.paths.documents_document_id_versions.post import CreateDocumentVersion
from synctera_client.paths.documents_document_id.get import GetDocument
from synctera_client.paths.documents_document_id_contents.get import GetDocumentContents
from synctera_client.paths.documents_document_id_versions_document_version.get import GetDocumentVersion
from synctera_client.paths.documents_document_id_versions_document_version_contents.get import GetDocumentVersionContents
from synctera_client.paths.documents.get import ListDocuments
from synctera_client.paths.documents_document_id.patch import UpdateDocument


class DocumentsApi(
    CreateDocument,
    CreateDocumentVersion,
    GetDocument,
    GetDocumentContents,
    GetDocumentVersion,
    GetDocumentVersionContents,
    ListDocuments,
    UpdateDocument,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
