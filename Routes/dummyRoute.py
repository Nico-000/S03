from fastapi import APIRouter, HTTPException, Security
from Config.jwtConfig import jwtConfig
from logging import getLogger
logger = getLogger("RequestLogger") 
dummy_router = APIRouter(prefix="/dummy", tags=["Dummy"])

@dummy_router.post(
    "/",
    summary="Crear un recurso dummy",
    description="Este endpoint permite crear un recurso dummy en el sistema. Es útil para pruebas y validación del funcionamiento de la API.",
    responses={
        201: {"description": "Recurso dummy creado exitosamente."},
        400: {"description": "Los datos proporcionados son inválidos."},
        401: {"description": "El usuario no está autenticado o no tiene permisos para realizar esta acción."},
        500: {"description": "Error inesperado al procesar la solicitud."}
    }
)
async def Metodo_Dummy(current_user: str = Security(jwtConfig.validate_token)):
    try:
        logger.info(f"Usuario {current_user} está intentando obtener datos de el endpoint Dummy.")
        pass
    except HTTPException as e:
        logger.error(f"HTTPException en login: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en login: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado al generar el token: {str(e)}")
