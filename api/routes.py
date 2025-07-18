from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from services.document_service import gerar_documento_docx, listar_variaveis_template_service
from core.exceptions import InvalidContextJSON
from docxtpl import DocxTemplate
from utils.file_utils import create_temp_dir, save_upload_file

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

@router.post("/variaveis-template/")
async def listar_variaveis_template(template_file: UploadFile = File(...)):
    try:
        return await listar_variaveis_template_service(template_file)
    except InvalidContextJSON:
        raise HTTPException(status_code=400, detail="JSON inválido.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", tags=["Status"])
def health_check():
    return {"status": "ok"}
