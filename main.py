from fastapi import FastAPI
from api.routes import router as api_router

app = FastAPI(
    title="JAAS - Jinja As An Service",
    description="Prova de conceito de um serviço jinja para geração de documentos, desacoplado da api principal",
    version="0.1"
)

app.include_router(api_router)
