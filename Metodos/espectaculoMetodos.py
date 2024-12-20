from Clases.espectaculoClass import espectaculoClass
from Metodos.OracleMetodos import OracleMetodos
import logging

# Configurar el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class espectaculoMetodos:
    @staticmethod
    def select_espectaculo(id_espectaculo, connection=None):
        cursorPython = None
        db = OracleMetodos()  # Instancia de la clase para manejar Oracle       
        local_connection = False  # Indica si la conexión fue creada localmente  

        try:
            logger.info(f"Intentando obtener el espectaculo con ID: {id_espectaculo}")

            if not connection:
                connection = db.connect()
                local_connection = True  # Marcar que la conexión fue creada localmente            

            cursorPython = connection.cursor()
            resultado_cursorOracle = db.create_ref_cursor(cursorPython)

            # Llamar al procedimiento almacenado
            cursorPython.callproc(
                "ESPECTACULOS_PRC_SELECT_ROW",
                [id_espectaculo, resultado_cursorOracle]
            )

            # Obtener el cursor devuelto por el procedimiento
            cursor_resultadoIntermediario = resultado_cursorOracle.getvalue()

            # Verificar si hay filas en el cursor
            rows = cursor_resultadoIntermediario.fetchone()
            if rows:
                logger.info(f"Película encontrada con ID: {id_espectaculo}")
                return espectaculoClass(rows[1], rows[2], rows[3],rows[4], rows[5], rows[6], rows[7], rows[8], id_espectaculo=rows[0], existe=True)
            
            # Retorna un objeto con existe=False si no hay datos
            logger.warning(f"No se encontró película con ID: {id_espectaculo}")
            return espectaculoClass(None, None, None, None, None, None, None, None, id_espectaculo=None, existe=False)

        except Exception as e:
            logger.error(f"Error al obtener la película con ID {id_espectaculo}: {e}")
            raise
        finally:
            if cursorPython:
                cursorPython.close()
            if local_connection and connection:
                connection.close()

    @staticmethod
    def espectaculo_guardar(espectaculo, connection=None):
        cursor = None
        db = OracleMetodos()  # Instancia de la clase para manejar Oracle
        local_connection = False  # Indica si la conexión fue creada localmente

        try:
            # Crear conexión si no se proporcionó una
            if connection is None:
                connection = db.connect()
                local_connection = True

            logger.info(f"Verificando existencia de la película con ID: {espectaculo.id_espectaculo}")
            espectaculo.existe = espectaculoMetodos.select_espectaculo(espectaculo.id_espectaculo, connection).existe

            cursorPython = connection.cursor()
            v_salida = cursorPython.var(int)  # Variable de salida para el ID generado o actualizado            

            # Determinar si es un INSERT o un UPDATE (no se actualizará información)
            if espectaculo.existe:
                logger.warning(f"La película con ID {espectaculo.id_espectaculo} ya existe.")
                return(f"No es posible actualizar el espectaculo con ID:{espectaculo.espectaculo}")
                
            else:
                procedimiento = "ESPECTACULOS_PRC_INSERT"
                params = [espectaculo.nombre_espectaculo, espectaculo.duracion, espectaculo.descripcion,espectaculo.usuario_creacion,espectaculo.fecha_creacion,espectaculo.ip,espectaculo.usuario_modificacion,espectaculo.fecha_modificacion,  v_salida]
                operacion = "insertado"
                logger.info(f"Creando un nuevo espectaculo: {espectaculo.titulo}")

            # Llamar al procedimiento almacenado
            cursorPython.callproc(procedimiento, params)

            # Obtener el ID generado o actualizado
            espectaculo.id_espectaculo = v_salida.getvalue()

            # Confirmar los cambios solo si la conexión fue creada localmente
            if local_connection:
                connection.commit()

            logger.info(f"Espectaculo {operacion} con éxito. ID: {espectaculo.id_espectaculo}")
            return espectaculo.id_espectaculo

        except Exception as e:
            # Hacer rollback si ocurre un error
            if connection and local_connection:
                connection.rollback()
            logger.error(f"Error al guardar o actualizar la película: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if local_connection and connection:
                connection.close()