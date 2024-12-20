from fastapi import APIRouter, HTTPException, Security
from typing import Optional
from logging import getLogger  # Importa el logger configurado globalmente
logger = getLogger("RequestLogger")  # Usa el logger configurado en el middleware
from Config.jwtConfig import jwtConfig
from Clases.pezClass import pezClass
from Metodos.pezMetodos import pezMetodos
from datetime import datetime
from Metodos.generalesMetodos import generalesMetodos

# Crear el router para Actores
pez_router = APIRouter(prefix="/pez", tags=["pez"])

@pez_router.get(
    "/{id_pez}",
    summary="Obtener información de un pez por ID",
    description="Este endpoint permite a un usuario autenticado proporcionar un ID único para obtener la información detallada de un actor específico.",
    responses={
        200: {"description": "Solicitud exitosa, retorna los detalles del pez."},
        400: {"description": "El ID del pez proporcionado no es válido."},
        401: {"description": "El usuario no está autenticado o el token es inválido."},
        404: {"description": "No se encontró un pez con el ID proporcionado."},
        500: {"description": "Error inesperado al procesar la solicitud."}
    }
)
async def get_pez_by_id(id_pez: str, current_user: str = Security(jwtConfig.validate_token)):
    """
    Endpoint para obtener los actores por ID.
    """
    try:
        logger.info(f"Usuario {current_user} solicitó el pez con ID: {id_pez}")
        
        if not id_pez.isdigit():
            logger.warning(f"ID del pez no válido: {id_pez}")
            raise HTTPException(status_code=400, detail="El id de pez debe ser un número válido.")
        
        pez = pezMetodos.select_pez(id_pez)
        if pez.existe:
            logger.info(f"Pez encontrado: {id_pez}")
            return {"success": True, "message": "Pez encontrado", "data": pez}
        else:
            logger.warning(f"No se encontró pez con ID: {id_pez}")
            return {"success": False, "message": "Actor no encontrado"}
    except HTTPException as e:
        logger.error(f"HTTPException en /pez: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en /pez: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado al obtener el pez: {str(e)}")


# Ruta para crear o actualizar una película
@pez_router.put(
    "/save",
    summary="Crear o actualizar un pez",
    description="Este endpoint permite a un usuario autenticado crear un nuevo actor o actualizar un actor existente.",
    responses={
        200: {"description": "Actor creado o actualizado con éxito."},
        400: {"description": "Los datos proporcionados no son válidos."},
        401: {"description": "El usuario no está autenticado o el token es inválido."},
        404: {"description": "No se encontró un actor con el ID proporcionado."},
        500: {"description": "Error inesperado al procesar la solicitud."}
    }
)
async def save_pez(
    nombre_pez: str,
    especie_pez: str,
    edad_pez: str,
    id_pez: Optional[str] = None,  # Pez ID ahora es opcional
    current_user: str = Security(jwtConfig.validate_token)
):
    """
    Endpoint para crear o actualizar un actor.
    Si se pasa un 'id', se actualizará el pez. Si no, se creará uno nuevo.
    """
    try:
        logger.info(f"Usuario {current_user} intentó guardar o actualizar el pez con ID: {id_pez}")
        logger.info(f"Datos del pez: nombre_pez={nombre_pez}, especie_pez={especie_pez}, edad_pez={edad_pez}, id_pez={id_pez}")

        # Si id_actor es None o 0, tratamos la solicitud como una creación
        if id_pez is None or id_pez == '0':
            logger.info("Creando un nuevo pez...")
        
        # Crear o actualizar un actor utilizando el método correspondiente
        pez = pezClass(
            nombre_pez=nombre_pez,
            especie_pez=especie_pez,
            edad_pez=edad_pez,
            usuario_creacion=current_user,
            fecha_creacion= datetime.now(),
            ip=generalesMetodos.getIP(),
            usuario_modificacion=current_user,
            fecha_modificacion= datetime.now(),
            id=id_pez if id_pez else 0  # Si no se pasa id, se asigna 0
        )
        
        # Llamar al método para guardar la película (crear o actualizar)
        id_pez = pezMetodos.pez_guardar(pez)

        if id_pez:
            logger.info(f"pez guardado/actualizado con éxito. ID: {id_pez}")
            return {"success": True, "message": f"Pez guardado con éxito. ID: {id_pez}", "data": {"id_pez": id_pez}}
        else:
            logger.warning(f"No se pudo guardar/actualizar el pez con ID: {id_pez}")
            raise HTTPException(status_code=400, detail="Error al guardar o actualizar el pez")

    except HTTPException as e:
        logger.error(f"HTTPException en /pez/save: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en /pez/save: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado al guardar o actualizar el pez: {str(e)}")