from logging import getLogger  # Importa el logger configurado globalmente
logger = getLogger("RequestLogger")  # Usa el logger configurado en el middleware
from Metodos.OracleMetodos import OracleMetodos
from Clases.pezEspectaculoRelClass import pezEspectaculoRelClass


class pezEspectaculoRelMetodos:
    @staticmethod
    def select_pezEspectaculoRel(id, connection = None):
        """
        Obtiene un peliculaActor específico usando peliculas_actores_prc_select_row.
        :param id: ID de la pelicula_actor a buscar.
        :return: Instancia de peliculasActoresClass con los datos obtenidos.
        """     
        cursorPython = None
        db = OracleMetodos()  # Instancia de la clase para manejar Oracle       
        
        local_connection = False  # Indica si la conexión fue creada localmente  
        try:
            if not connection:
                connection = db.connect()
                local_connection = True  # Marcar que la conexión fue creada localmente           
            
            cursorPython = connection.cursor()
            resultado_cursorOracle = db.create_ref_cursor(cursorPython)

            # Llamar al procedimiento almacenado
            cursorPython.callproc(
                "pez_Espectaculo_Rel_prc_select_row",
                [id, resultado_cursorOracle]
            )
            
            # Obtener el cursor devuelto por el procedimiento
            cursor_resultadoIntermediario = resultado_cursorOracle.getvalue()

            # Verificar si hay filas en el cursor
            rows = cursor_resultadoIntermediario.fetchone()
            if rows:
                return pezEspectaculoRelClass(rows[1], rows[2], rows[3],rows[4], rows[5], rows[6], rows[7], rows[8], id_pez_espectaculo=rows[0], existe=True)
            
            # Retorna un objeto con existe=False si no hay datos
            return pezEspectaculoRelClass(None, None, None, None, None, None,None,None, actor_id=None, existe=False)
            
        except Exception as e:
            print(f"Error al obtener la pelicula_actor: {e}")
            raise
        finally:
            # Cerrar el cursor
            if cursorPython:
                cursorPython.close()
            # Si la conexión fue creada localmente, cerrarla
            if local_connection and connection:
                connection.close()
    
    @staticmethod
    def pezEspectaculoRel_guardar(pezEspectaculoRel, connection=None):
        """
        Inserta o actualiza una peliculaActor según el valor de `peliculaActor.existe`.
        :param peliculaActor: Instancia de peliculasActoresClass.
        :param connection: Conexión activa opcional.
        :return: ID generado o actualizado de la peliculaActor.
        """
        cursor = None
        db = OracleMetodos()  # Instancia de la clase para manejar Oracle
        local_connection = False  # Indica si la conexión fue creada localmente

        try:
            # Crear conexión si no se proporcionó una
            if connection is None:
                connection = db.connect()
                local_connection = True

            # Crear el cursor
            cursorPython = connection.cursor()
            v_salida = cursorPython.var(int)  # Variable de salida para el ID generado o actualizado

            # Determinar si es un INSERT o un UPDATE
            if pezEspectaculoRel.existe:
                return(f"No es posible actualizar la pelicula_actor con ID:{pezEspectaculoRel.id}")
            
            else:
                procedimiento = "PECES_ESPECTACULOS_Rel_PRC_INSERT"
                params = [pezEspectaculoRel.id_pez, pezEspectaculoRel.id_espectaculo, pezEspectaculoRel.fecha_participacion, pezEspectaculoRel.usuario_creacion, pezEspectaculoRel.fecha_creacion,id_pez_espectaculo.ip,id_pez_espectaculo.usuario_modificacion,id_pez_espectaculo.fecha_modificacion, v_salida]
                #self, id_pez, id_espectaculo, fecha_participacion, 
                 #usuario_creacion=None, fecha_creacion=None, 
                 #ip=None, usuario_modificacion=None, fecha_modificacion=None, existe=False):
                operacion = "insertado"

            # Llamar al procedimiento almacenado
            cursorPython.callproc(procedimiento, params)

            # Obtener el ID generado o actualizado
            id_pez_espectaculo = v_salida.getvalue()

            # Confirmar los cambios solo si la conexión fue creada localmente
            if local_connection:
                connection.commit()

            print(f"pez_espectaculo {operacion} con éxito. ID: {id_pez_espectaculo}")
            return id_pez_espectaculo

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