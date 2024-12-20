from Clases.pezClass import pezClass
from Metodos.OracleMetodos import OracleMetodos
import logging


#Configurar el Logger
logger= logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler= logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter= logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class pezMetodos:
    @staticmethod
    def select_pez(id_pez, connection = None):
        cursorPython = None
        db = OracleMetodos()  # Instancia de la clase para manejar Oracle      
        local_connection = False  # Indica si la conexión fue creada localmente  
    

        try:
            logger.info(f"Obteniendo el pez con ID: {id_pez}")
            
            if not connection:
                connection = db.connect()
                local_connection = True  # Marcar que la conexión fue creada localmente          
           
            cursorPython = connection.cursor()
            resultado_cursorOracle = db.create_ref_cursor(cursorPython)


            # Llamar al procedimiento almacenado
            cursorPython.callproc(
                "peces_prc_select_row",
                [id_pez, resultado_cursorOracle]
            )
           
            # Obtener el cursor devuelto por el procedimiento
            cursor_resultadoIntermediario = resultado_cursorOracle.getvalue()


            # Verificar si hay filas en el cursor
            rows = cursor_resultadoIntermediario.fetchone()
            if rows:
                return pezClass(rows[1], rows[2], rows[3],rows[4], rows[5], rows[6], rows[7], rows[8], id_pez=rows[0], existe=True)
           
            # Retorna un objeto con existe=False si no hay datos
            return pezClass(None, None, None, None, None, None, None, None, id_pez=None, existe=False)
           
        except Exception as e:
            print(f"Error al obtener el pez: {e}")
            raise
        finally:
            # Cerrar el cursor
            if cursorPython:
                cursorPython.close()
            # Si la conexión fue creada localmente, cerrarla
            if local_connection and connection:
                connection.close()
   
@staticmethod
def pez_guardar(pez, connection=None):
    """
    Inserta o actualiza un actor según el valor de `pez.existe`.
    :param pez: Instancia de pezClass.
    :param connection: Conexión activa opcional.
    :return: ID generado o actualizado del actor.
    """
    cursor = None
    db = OracleMetodos()  # Instancia de la clase para manejar Oracle
    local_connection = True  # Indica si la conexión fue creada localmente

    try:
        # Crear conexión si no se proporcionó una
        if connection is None:
            connection = db.connect()
            local_connection = True

        logger.info(f"Verificando existencia del pez con ID: {pez.id_pez}")
        pezBD= pezMetodos.select_pez(pez.id_pez, connection)

        # Crear el cursor
        cursorPython = connection.cursor()
        v_salida = cursorPython.var(int)  # Variable de salida para el ID generado o actualizado

        # Determinar si es un INSERT o un UPDATE
        if pezBD.existe:
            procedimiento = "PECES_PRC_UPDATE"
            pez.usuario_creacion = pezBD.usuario_creacion
            pez.fecha_creacion = pezBD.fecha_creacion
            params = [
                pez.id_pez,
                pez.nombre_pez,
                pez.especie_pez,
                pez.edad_pez,
                pez.usuario_modificacion,
                pez.fecha_modificacion,
                pez.ip,
                v_salida 
                ]
            return(f"No es posible actualizar el pez con ID:{pez.id_pez}")
        
        else:
            procedimiento = "PECES_PRC_INSERT"
            params = [pez.nombre_pez, pez.especie_pez, pez.edad_pez,pez.usuario_creacion,pez.fecha_creacion,pez.ip, pez.usuario_modificacion, pez.fecha_modificacion, v_salida]
            operacion = "insertado"

        # Llamar al procedimiento almacenado
        cursorPython.callproc(procedimiento, params)

        # Obtener el ID generado o actualizado
        pez.id_pez = v_salida.getvalue()

        # Confirmar los cambios solo si la conexión fue creada localmente
        if local_connection:
            connection.commit()

        print(f"pez {operacion} con éxito. ID: {pez.id_pez}")
        return pez.id_pez

    except Exception as e:
        # Hacer rollback si ocurre un error
        if connection and local_connection:
            connection.rollback()          
        raise
    finally:
        # Cerrar el cursor si fue creado
        if cursor:
            cursor.close()

        # Cerrar la conexión si fue creada localmente
        if local_connection and connection:
            connection.close()