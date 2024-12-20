from fastapi import APIRouter, HTTPException, Security
from typing import Optional
from logging import getLogger  # Importa el logger configurado globalmente
from Metodos.jwtMetodos import jwtMetodos
from Clases.espectaculoClass import espectaculoClass
from Metodos.espectaculoMetodos import espectaculoMetodos
logger = getLogger("RequestLogger")  # Usa el logger configurado en el middleware

# Crear el router para Peliculas
espectaculo_router = APIRouter(prefix="/Espectaculos", tags=["Espectaculos"])

@espectaculo_router.get(
    "/{espectaculo_id}",
    summary="Obtener información de un espectaculo por ID",
    description="Este endpoint permite a un usuario autenticado proporcionar un ID único para obtener la información detallada de una película específica.",
    responses={
        200: {"description": "Solicitud exitosa, retorna los detalles de la película."},
        400: {"description": "El ID de la película proporcionado no es válido."},
        401: {"description": "El usuario no está autenticado o el token es inválido."},
        404: {"description": "No se encontró una película con el ID proporcionado."},
        500: {"description": "Error inesperado al procesar la solicitud."}
    }
)
async def get_espectaculo_by_id(id_espectaculo: str, current_user: str = Security(jwtMetodos.validate_token)):
    """
    Endpoint para obtener las Películas por ID.
    """
    try:
        logger.info(f"Usuario {current_user} solicitó la película con ID: {id_espectaculo}")
        
        if not id_espectaculo.isdigit():
            logger.warning(f"ID de película no válido: {id_espectaculo}")
            raise HTTPException(status_code=400, detail="El id de película debe ser un número válido.")
        
        espectaculo = espectaculoMetodos.select_espectaculo(id_espectaculo)
        if espectaculo.existe:
            logger.info(f"Película encontrada: {espectaculo}")
            return {"success": True, "message": "Película encontrada", "data": espectaculo}
        else:
            logger.warning(f"No se encontró pelicula con ID: {id_espectaculo}")
            return {"success": False, "message": "Película no encontrada"}
    except HTTPException as e:
        logger.error(f"HTTPException en /películas: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en /películas: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado al obtener la película: {str(e)}")


# Ruta para crear o actualizar una película
@espectaculo_router.put(
    "/save",
    summary="Crear o actualizar un espectaculo",
    description="Este endpoint permite a un usuario autenticado crear una nuevo espectaculo o actualizar un espectaculo existente.",
    responses={
        200: {"description": "espectaculo creado o actualizada con éxito."},
        400: {"description": "Los datos proporcionados no son válidos."},
        401: {"description": "El usuario no está autenticado o el token es inválido."},
        404: {"description": "No se encontró una película con el ID proporcionado."},
        500: {"description": "Error inesperado al procesar la solicitud."}
    }
)

async def save_espectaculo(
    nombre_espectaculo: str, 
    duracion: int, 
    descripcion: str, 
    id_espectaculo: Optional[str] = None,  # Película ID ahora es opcional
    current_user: str = Security(jwtMetodos.validate_token)
):
    """
    Endpoint para crear o actualizar una película.
    Si se pasa un `id`, se actualizará la película. Si no, se creará una nueva.
    """
    try:
        logger.info(f"Usuario {current_user} intentó guardar o actualizar la película con ID: {id_espectaculo}")

        # Si id es None o 0, tratamos la solicitud como una creación
        if id_espectaculo is None or id_espectaculo == '0':
            logger.info("Creando una nueva película...")
        
        # Crear o actualizar la película utilizando el método correspondiente
        espectaculo = espectaculoClass(
            nombre_espectaculo=nombre_espectaculo,
            duracion=duracion,
            descripcion=descripcion,
            id_espectaculo=id_espectaculo if id_espectaculo else 0  # Si no se pasa id, se asigna 0
        )
        
        # Llamar al método para guardar la película (crear o actualizar)
        id_espectaculo = espectaculoMetodos.espectaculo_guardar(espectaculo)

        if id_espectaculo:
            logger.info(f"Película guardada/actualizada con éxito. ID: {id_espectaculo}")
            return {"success": True, "message": f"Película guardada con éxito. ID: {id_espectaculo}", "data": {"película_id": id_espectaculo}}
        else:
            logger.warning(f"No se pudo guardar/actualizar la película con ID: {id_espectaculo}")
            raise HTTPException(status_code=400, detail="Error al guardar o actualizar la película")

    except HTTPException as e:
        logger.error(f"HTTPException en /películas/save: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en /películas/save: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado al guardar o actualizar la película: {str(e)}")
