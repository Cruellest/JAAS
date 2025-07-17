import json
import os
import tempfile
import shutil  
from typing import Dict

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from starlette import status

from docxtpl import DocxTemplate

app = FastAPI(
    title="JAAS - Jinja As An Service",
    description="Prova de conceito de um serviço jinja para geração de documentos, desacoplado da api principal",
    version="0.1"
)

@app.post(
    "/gerar-documento/",
    summary="Gera um documento DOCX a partir de um template e dados JSON",
    tags=["Documentos"]
)
async def gerar_documento(
    background_tasks: BackgroundTasks,
    template_file: UploadFile = File(..., description="Arquivo de template .docx"),
    context_json: str = Form(..., description='Objeto JSON (como string) contendo as variáveis para o template. Ex: \'{"chave": "valor"}\'')
):
    try:
        context: Dict = json.loads(context_json)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O 'context_json' fornecido não é um JSON válido."
        )
        
    temp_dir = tempfile.mkdtemp()
    try:
        template_path = os.path.join(temp_dir, template_file.filename)
        output_path = os.path.join(temp_dir, f"gerado_{template_file.filename}")

        try:
            with open(template_path, "wb") as buffer:
                buffer.write(await template_file.read())
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Não foi possível salvar o arquivo de template."
            )

        doc = DocxTemplate(template_path)
        doc.render(context)
        doc.save(output_path)

        background_tasks.add_task(shutil.rmtree, temp_dir)

        return FileResponse(
            path=output_path,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            filename=f"documento_gerado.docx"
        )
    except Exception as e:
        shutil.rmtree(temp_dir)
        raise e


@app.get("/health", summary="Verifica a saúde da API", tags=["Status"])
def health_check():
    return {"status": "ok"}