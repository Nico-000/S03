from fastapi import APIRouter, HTTPException, Security
from logging import getLogger  # Importa el logger configurado globalmente
logger = getLogger("RequestLogger")  # Usa el logger configurado en el middleware
from typing import Optional
from Metodos.jwtMetodos import jwtMetodos
from Clases.pezEspectaculoRelClass import pezEspectaculoRelClass
from Metodos.pezEspectaculoRelMetodos import pezEspectaculoRelMetodos
from datetime import datetime
from Metodos.generalesMetodos import generalesMetodos
# Crear el router para PeliculasActores
pezEspectaculoRel_router = APIRouter(prefix="/PeliculasActores", tags=["PeliculasActores"])

@pezEspectaculoRel_router.get(
    "/{peliculasActores_id}",
    summary="Obtener información de películas_actores por ID",
    description="Este endpoint permite a un usuario autenticado proporcionar un ID único para obtener la información detallada de una película_actor específica.",
    responses={
        200: {"description": "Solicitud exitosa, retorna los detalles de la película_actor."},
        400: {"description": "El ID de la película_actor proporcionado no es válido."},
        401: {"description": "El usuario no está autenticado o el token es inválido."},
        404: {"description": "No se encontró una película_actor con el ID proporcionado."},
        500: {"description": "Error inesperado al procesar la solicitud."}
    }
)
async def get_pelicula_actor_by_id(id: str, current_user: str = Security(jwtMetodos.validate_token)):
    """
    Endpoint para obtener las Películas_actores por ID.
    """
    try:
        logger.info(f"Usuario {current_user} solicitó la película_actor con ID: {id}")
        
        if not id.isdigit():
            logger.warning(f"ID de película_actor no válido: {id}")
            raise HTTPException(status_code=400, detail="El id de película_actor debe ser un número válido.")
        
        pezEspectaculoRel = pezEspectaculoRelMetodos.select_pezEspectaculoRel(id)
        if pezEspectaculoRel.existe:
            logger.info(f"Película_actor encontrada: {pezEspectaculoRel}")
            return {"success": True, "message": "Película_actor encontrada", "data": pezEspectaculoRel}
        else:
            logger.warning(f"No se encontró pelicula_actor con ID: {id}")
            return {"success": False, "message": "Película_actor no encontrada"}
    except HTTPException as e:
        logger.error(f"HTTPException en /películas_actores: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en /películas_actores: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado al obtener la película_actor: {str(e)}")


# Ruta para crear o actualizar una película
@pezEspectaculoRel_router.put(
    "/save",
    summary="Crear o actualizar una película_actor",
    description="Este endpoint permite a un usuario autenticado crear una nueva película_actor o actualizar una película_actor existente.",
    responses={
        200: {"description": "Película_actor creada o actualizada con éxito."},
        400: {"description": "Los datos proporcionados no son válidos."},
        401: {"description": "El usuario no está autenticado o el token es inválido."},
        404: {"description": "No se encontró una película_actor con el ID proporcionado."},
        500: {"description": "Error inesperado al procesar la solicitud."}
    }
)

async def save_pezEspectaculoRel(
    id_pez: str,
    id_espectaculo: str,
    fecha_participacion: str,
    id: Optional[str] = None,  # Película ID ahora es opcional
    current_user: str = Security(jwtMetodos.validate_token)
):
    """
    Endpoint para crear o actualizar una película_actor.
    Si se pasa un `id`, se actualizará la película_actor. Si no, se creará una nueva.
    """
    try:
        logger.info(f"Usuario {current_user} intentó guardar o actualizar la película_actor con ID: {id}")

        # Si id es None o 0, tratamos la solicitud como una creación
        if id is None or id == '0':
            logger.info("Creando una nueva película_actor...")
        
        # Crear o actualizar la película utilizando el método correspondiente
        pezEspectaculoRel = pezEspectaculoRelClass(
            id_pez = id_pez,
            id_espectaculo = id_espectaculo,
            fecha_participacion = fecha_participacion,
            usuario_creacion=current_user,
            fecha_creacion= datetime.now(),
            ip=generalesMetodos.getIP(),
            usuario_modificacion=current_user,
            fecha_modificacion= datetime.now(),
            id=id if id else 0  # Si no se pasa id, se asigna 0
        )
        
        # Llamar al método para guardar la película (crear o actualizar)
        id = pezEspectaculoRelMetodos.pezEspectaculoRel_guardar(pezEspectaculoRel)

        if id:
            logger.info(f"Película_actor guardada/actualizada con éxito. ID: {id}")
            return {"success": True, "message": f"Película_actor guardada con éxito. ID: {id}", "data": {"id": id}}
        else:
            logger.warning(f"No se pudo guardar/actualizar la película_actor con ID: {id}")
            raise HTTPException(status_code=400, detail="Error al guardar o actualizar la película_actor")

    except HTTPException as e:
        logger.error(f"HTTPException en /películas_actores/save: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado en /películas_actores/save: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado al guardar o actualizar la película_actor: {str(e)}")
