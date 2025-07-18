from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.responses import FileResponse
from fastapi import status
from pydantic import BaseModel
from app.services.document_service import gerar_documento_docx, listar_variaveis_template_service
from app.core.exceptions import InvalidContextJSON

router = APIRouter()

class VariaveisResponse(BaseModel):
    variaveis: list[str]

@router.post(
    "/gerar-documento/",
    tags=["Documentos"],
    summary="Gera um documento .docx a partir de um template e contexto",
    description="Essa rota recebe um arquivo template `.docx` e um JSON de contexto, preenchendo o template e retornando o documento final.",
    responses={
        200: {"content": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document": {}}},
        400: {"description": "JSON inválido."},
        500: {"description": "Erro interno no servidor."}
    }
)
async def gerar_documento(
    background_tasks: BackgroundTasks,
    template_file: UploadFile = File(..., description="Arquivo .docx com variáveis Jinja2"),
    context_json: str = Form(..., description="Contexto em JSON como string")
):
    try:
        return await gerar_documento_docx(template_file, context_json, background_tasks)
    except InvalidContextJSON:
        raise HTTPException(status_code=400, detail="JSON inválido.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/variaveis-template/",
    tags=["Documentos"],
    summary="Lista variáveis não declaradas de um template .docx",
    description="Recebe um template `.docx` e retorna as variáveis Jinja2 encontradas no documento.",
    response_model=VariaveisResponse,
    responses={
        200: {"description": "Lista de variáveis encontradas"},
        400: {"description": "Template inválido"},
        500: {"description": "Erro interno no servidor"}
    }
)
async def listar_variaveis_template(template_file: UploadFile = File(..., description="Template .docx com variáveis Jinja2")):
    try:
        return await listar_variaveis_template_service(template_file)
    except InvalidContextJSON:
        raise HTTPException(status_code=400, detail="JSON inválido.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/health",
    tags=["Status"],
    summary="Verifica o status da API",
    description="Retorna um JSON simples indicando que a API está funcionando.",
    response_model=dict
)
def health_check():
    return {"status": "ok"}
