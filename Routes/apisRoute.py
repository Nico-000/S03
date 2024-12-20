import httpx
from fastapi import APIRouter, HTTPException, Security
from Config.jwtConfig import jwtConfig
import logging

# Configurar el logger
logger = logging.getLogger(__name__)

# Crear el router para apis
apis_router = APIRouter(prefix="/apis", tags=["Apis"])

# Endpoint que consume la API de universidades
@apis_router.get(
    "/getApiDummy",
    summary="Crear un recurso dummy",
    description="Este endpoint permite crear un recurso dummy en el sistema. Es útil para pruebas y validación del funcionamiento de la API.",
    responses={
        201: {"description": "Recurso dummy creado exitosamente."},
        400: {"description": "Los datos proporcionados son inválidos."},
        401: {"description": "El usuario no está autenticado o no tiene permisos para realizar esta acción."},
        500: {"description": "Error inesperado al procesar la solicitud."}
    }
)
async def get_dummy(current_user: str = Security(jwtConfig.validate_token)):
    try:
        logger.info(f"Usuario {current_user} está intentando obtener datos de el endpoint Dummy.")
        pass    
    except httpx.RequestError as e:
        logger.error(f"Error de conexión con la API externa: {e}")
        raise HTTPException(status_code=500, detail="Error al conectar con el servidor externo")
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")