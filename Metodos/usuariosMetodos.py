from Metodos.logDataMetodos import logDataMetodos 
from Config.oracleConfig import oracleConfig
from Clases.usuariosClass import usuariosClass
from Metodos.generalesMetodos import generalesMetodos

class usuariosMetodos:

    @staticmethod
    def loginUsuarios(rut, password):
        """
        Obtiene un personaje específico usando personajes_prc_select_row.
        :param personaje_id: ID del personaje a buscar.
        :return: Instancia de PersonajesClass con los datos obtenidos.
        """     
        cursorPython = None
        connection = oracleConfig().connect()
        try:
            cursorPython = connection.cursor()
            resultado_cursorOracle = oracleConfig().create_ref_cursor(cursorPython)

            cursorPython.callproc(
                "USUARIOS_PRC_SELECT_ROW_RUT",
                [rut, resultado_cursorOracle]
            )
        
            # Obtener el cursor devuelto por el procedimiento
            cursor_resultadoIntermediario = resultado_cursorOracle.getvalue()

            # Verificar si hay filas en el cursor
            rows = cursor_resultadoIntermediario.fetchone()
            if rows:
                stored_hash = rows[5]
                if generalesMetodos.verify_password(stored_hash, password):
                    return usuariosClass(rows[1], rows[2], rows[3], rows[4], stored_hash, rows[6], id=rows[0], existe=True)
            
            # Retorna un objeto con existe=False si no hay datos
            return usuariosClass(None, None, None, None, None, None, None, existe=False)
        except Exception as e:
            print(f"Error al obtener el personaje: {e}")
            raise
        finally:
            # Cerrar el cursor
            if cursorPython:
                cursorPython.close()
            connection.close()

    @staticmethod
    def select_usuario_rut(rut, connection=None):
        """
        Obtiene un usuario específico usando el procedimiento almacenado USUARIOS_PRC_SELECT_ROW_RUT.
        :param rut: RUT del usuario a buscar.
        :param connection: Conexión activa opcional.
        :return: Instancia de usuariosClass con los datos obtenidos o existe=False si no hay resultados.
        """
        cursorPython = None
        db = oracleConfig()  # Instancia de la clase para manejar Oracle       
        local_connection = False  # Indica si la conexión fue creada localmente
        
        try:
            if not connection:
                connection = db.connect()
                local_connection = True  # Marcar que la conexión fue creada localmente           
            
            cursorPython = connection.cursor()
            resultado_cursorOracle = db.create_ref_cursor(cursorPython)

            # Llamar al procedimiento almacenado
            cursorPython.callproc(
                "USUARIOS_PRC_SELECT_ROW_RUT",
                [rut, resultado_cursorOracle]
            )
            
            # Obtener el cursor devuelto por el procedimiento
            cursor_resultadoIntermediario = resultado_cursorOracle.getvalue()

            # Verificar si hay filas en el cursor
            rows = cursor_resultadoIntermediario.fetchone()
            if rows:
                return usuariosClass(rows[1], rows[2], rows[3], rows[4], rows[5], rows[6], rows[7], rows[8], rows[9], rows[10], rows[11], id=rows[0], existe=True)
            
            # Retorna un objeto con existe=False si no hay datos
            return usuariosClass(None, None, None, None, None, existe=False)
            
        except Exception as e:
            print(f"Error al obtener la película: {e}")
            raise
        finally:
            # Cerrar el cursor
            if cursorPython:
                cursorPython.close()
            # Si la conexión fue creada localmente, cerrarla
            if local_connection and connection:
                connection.close()

    @staticmethod
    def usuario_guardar(usuario, connection=None):
        """
        Inserta o actualiza un usuario en la base de datos según su existencia en el sistema.
        
        Si el usuario existe (determinado por su RUT), se actualizan sus datos. 
        Si no existe, se inserta como un nuevo registro.
        
        :param usuario: Instancia de usuariosClass con los datos del usuario.
        :param connection: Objeto de conexión activo a la base de datos. Si no se proporciona, se creará una conexión local.
        :return: ID generado o actualizado del usuario.
        """
        cursorPython = None
        db = oracleConfig()  # Instancia para manejar conexiones Oracle.
        local_connection = False  # Indica si la conexión fue creada localmente.

        try:
            # 1. Crear conexión si no se proporcionó una
            if connection is None:
                connection = db.connect()
                local_connection = True

            # 2. Crear un cursor para la ejecución de SQL
            cursorPython = connection.cursor()
            v_salida = cursorPython.var(int)  # Variable de salida para el ID generado/actualizado.

            # 3. Verificar si el usuario existe en la base de datos
            usuarioDesdeBD = usuariosMetodos.select_usuario_rut(usuario.rut, connection)

            # 4. Determinar si es un INSERT o un UPDATE según la existencia del usuario
            if usuarioDesdeBD.existe:
                # Configuración para una actualización (UPDATE)
                procedimiento = "USUARIOS_PRC_UPDATE"
                usuario.usuario_modificacion = usuarioDesdeBD.usuario_modificacion
                usuario.fecha_modificacion = usuarioDesdeBD.fecha_modificacion
                usuario.existe = usuarioDesdeBD.existe
                password_hash = generalesMetodos.hash_password(usuario.password_plain)
                valorAnterior = generalesMetodos.objeto_a_json(usuarioDesdeBD)  # Estado anterior del usuario.

                params = [usuario.id,
                        usuario.rut,
                        usuario.nombre, 
                        usuario.apellido, 
                        usuario.estado, 
                        password_hash,
                        usuario.password_plain,
                        usuario.usuario_creacion,
                        usuario.fecha_creacion,
                        usuario.ip,
                        usuario.usuario_modificacion,
                        usuario.fecha_modificacion,
                        v_salida]
                operacion = "actualizada"  # Mensaje de operación.

            else:
                # Configuración para una inserción (INSERT)
                procedimiento = "USUARIOS_PRC_INSERT"
                valorAnterior = "Nuevo Registro"  # No existe un estado anterior.
                password_hash = generalesMetodos.hash_password(usuario.password_plain)

                params = [usuario.rut,
                        usuario.nombre, 
                        usuario.apellido,  
                        usuario.estado, 
                        password_hash,
                        usuario.password_plain,
                        usuario.usuario_creacion,
                        usuario.fecha_creacion,
                        usuario.ip,
                        usuario.usuario_modificacion,
                        usuario.fecha_modificacion,
                        v_salida]
                operacion = "insertada"  # Mensaje de operación.

            # 5. Ejecutar el procedimiento almacenado con los parámetros
            cursorPython.callproc(procedimiento, params)

            # 6. Obtener el ID generado o actualizado del procedimiento
            usuario.id = v_salida.getvalue()

            # 7. Insertar un registro en el log de auditoría
            valorNuevo = generalesMetodos.objeto_a_json(usuario)  # Estado actualizado del usuario.
            logDataMetodos.insertLog(valorAnterior, valorNuevo, connection)

            # 8. Confirmar los cambios si la conexión fue creada localmente
            if local_connection:
                connection.commit()

            print(f"Usuario {operacion} con éxito. ID: {usuario.id}")
            return usuario.id

        except Exception as e:
            # Hacer rollback si ocurre un error y la conexión fue creada localmente
            if connection and local_connection:
                connection.rollback()
            print(f"Error al guardar el usuario: {e}")
            raise
        finally:
            # 9. Cerrar el cursor si fue creado
            if cursorPython:
                cursorPython.close()

            # 10. Cerrar la conexión si fue creada localmente
            if local_connection and connection:
                connection.close()
