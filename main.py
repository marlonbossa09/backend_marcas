import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database.db import Base, engine
from routers import marcas
from auth import auth_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Registro de Marcas API", swagger_ui_parameters={"syntaxHighlight": False})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errores = []
    for error in exc.errors():
        errores.append({
            "campo": ".".join(str(x) for x in error["loc"]),
            "mensaje": error["msg"]
        })
    return JSONResponse(
        status_code=422,
        content={"errores": errores}
    )

app.include_router(marcas.router)
app.include_router(auth_router.router, prefix="/auth")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)