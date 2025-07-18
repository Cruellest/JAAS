import json
from typing import Dict
from fastapi import UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate

from core.exceptions import InvalidContextJSON
from utils.file_utils import create_temp_dir, save_upload_file, remove_dir


async def gerar_documento_docx(
    template_file: UploadFile,
    context_json: str,
    background_tasks: BackgroundTasks
):
    try:
        context: Dict = json.loads(context_json)
    except json.JSONDecodeError:
        raise InvalidContextJSON()

    temp_dir = create_temp_dir()
    try:
        template_path = await save_upload_file(template_file, temp_dir)
        output_path = template_path.replace(".docx", "_output.docx")

        doc = DocxTemplate(template_path)
        doc.render(context)
        doc.save(output_path)

        background_tasks.add_task(remove_dir, temp_dir)

        return FileResponse(
            path=output_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename="documento_gerado.docx"
        )
    except Exception as e:
        remove_dir(temp_dir)
        raise e

async def listar_variaveis_template_service(template_file: UploadFile):
    temp_dir = create_temp_dir()
    try:
        path = await save_upload_file(template_file, temp_dir)
        doc = DocxTemplate(path)
        return {"variaveis": list(doc.get_undeclared_template_variables({}))}
    finally:
        remove_dir(temp_dir)