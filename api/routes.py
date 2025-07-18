from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from services.document_service import gerar_documento_docx
from core.exceptions import InvalidContextJSON

router = APIRouter()

@router.post("/gerar-documento/", tags=["Documentos"])
async def gerar_documento(
    background_tasks: BackgroundTasks,
    template_file: UploadFile = File(...),
    context_json: str = Form(...)
):
    try:
        return await gerar_documento_docx(template_file, context_json, background_tasks)
    except InvalidContextJSON:
        raise HTTPException(status_code=400, detail="JSON inválido.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", tags=["Status"])
def health_check():
    return {"status": "ok"}
