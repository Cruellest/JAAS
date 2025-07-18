from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.routes import router as api_router

app = FastAPI(
    title="JAAS - Jinja As An Service",
    description="Prova de conceito de um serviço jinja para geração de documentos, desacoplado da api principal",
    version="0.3"
)

app.include_router(api_router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")