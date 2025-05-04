from renderer_definition.tasks import render_pdf_task
from renderer_definition.models import (
    Document as DocumentIR,
    RenderedDocument
)
from app.dependencies.user import ActiveUserAnnotation
from .router import router


@router.get(
    path='/{document_id}/render',
    response_model=RenderedDocument
)
async def render_document(user: ActiveUserAnnotation, document_id: str):
    result = render_pdf_task.delay(
        DocumentIR(
            name="asdfsadf",
            content=[],
            style="",
        ).dict()
    )
    return RenderedDocument(**result.get(timeout=10))
