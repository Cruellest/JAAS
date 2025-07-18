import os
import tempfile
import shutil
from fastapi import UploadFile

def create_temp_dir() -> str:
    return tempfile.mkdtemp()

async def save_upload_file(upload_file: UploadFile, destination_dir: str) -> str:
    file_path = os.path.join(destination_dir, upload_file.filename)
    with open(file_path, "wb") as f:
        f.write(await upload_file.read())
    return file_path

def remove_dir(path: str):
    shutil.rmtree(path, ignore_errors=True)
