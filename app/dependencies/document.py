from fastapi import Depends, status
import typing

from app.models.document import Document, DocumentAccessRole
from ._context import ContextAnnotation, get_context_based_exception
from .repository import DocumentsRepositoryAnnotation
from .user import ActiveUserAnnotation


async def document_dependency(
    context: ContextAnnotation,
    repository: DocumentsRepositoryAnnotation,
    document_id: str,
) -> Document:
    document = await repository.get_document(
        id=document_id,
        owner_id=None
    )
    if document is None:
        raise get_context_based_exception(
            context=context,
            http_code=status.HTTP_404_NOT_FOUND,
            ws_code=status.WS_1002_PROTOCOL_ERROR,
            message=f"document {document_id} not found"
        )

    return Document.model_validate(document)


DocumentAnnotation = typing.Annotated[
    Document,
    Depends(document_dependency)
]


def document_user_role_dependency(
    context: ContextAnnotation,
    user: ActiveUserAnnotation,
    document: DocumentAnnotation,
) -> DocumentAccessRole:
    if document.owner_id == user.id:
        return DocumentAccessRole.EDITOR

    for restriction in document.access_restrictions:
        if user.id == restriction.user_id:
            return restriction.rule

    raise get_context_based_exception(
        context=context,
        http_code=status.HTTP_403_FORBIDDEN,
        ws_code=status.WS_1008_POLICY_VIOLATION,
        message=f"access denied for document {document.id}"
    )


DocumentUserRoleAnnotation = typing.Annotated[
    DocumentAccessRole,
    Depends(document_user_role_dependency)
]
