from fastapi import APIRouter, HTTPException
from logging import getLogger
from Metodos.usuariosMetodos import usuariosMetodos
from Metodos.generalesMetodos import generalesMetodos
from Clases.usuariosClass import usuariosClass
from datetime import datetime
logger = getLogger("RequestLogger") 

# Crear el router para user
user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.post(
    "/Save",
    summary="Método para crear un nuevo usuario",
    description="Este método permite a un administrador crear un nuevo usuario proporcionando un nombre de usuario y una contraseña.",
    responses={
        201: {"description": "Usuario creado exitosamente"},
        400: {"description": "Datos de entrada inválidos"},
        500: {"description": "Error inesperado"}
    }
)
async def create_user(username: str, password: str, nombre: str, apellido: str):
    """
    Endpoint para crear un nuevo usuario.
    """
    try:
        logger.info(f"Intento de crear usuario con username: {username}")

        if not username.isdigit():
            logger.warning(f"El username ingresado no es válido: {username}")
            raise HTTPException(status_code=400, detail="El nombre de usuario debe ser un número válido.")

        # Suponemos que existe una función para agregar usuarios en 'usuariosMetodos'
        
        usuario = usuariosClass(username, nombre, apellido,'1',None,password, username, datetime.now(),generalesMetodos.getIP(), username, datetime.now())
        result = usuariosMetodos.usuario_guardar(usuario)

        if result:
            logger.info(f"Usuario creado con éxito: {username}")
            return {"success": True, "message": "Usuario creado exitosamente"}
        else:
            logger.warning(f"No se pudo crear el usuario con username: {username}")
            return {"success": False, "message": "No se pudo crear el usuario, posiblemente ya exista"}

    except HTTPException as e:
        logger.error(f"HTTPException al crear usuario: {e}")
        raise e
    except Exception as e:
        logger.error(f"Error inesperado al crear usuario: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado al crear el usuario: {str(e)}")