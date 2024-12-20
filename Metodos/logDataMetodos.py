from datetime import datetime

class logDataMetodos:

    @staticmethod
    def insertLog(valorAnterior, valorNuevo, connection):
        """
        Inserta un registro en la tabla logData utilizando un procedimiento almacenado.
        
        :param valorAnterior: Valor previo que se desea registrar (VARCHAR2).
        :param valorNuevo: Nuevo valor que se desea registrar (VARCHAR2).
        :param connection: Conexión activa a la base de datos Oracle.
        :return: None. Imprime un mensaje de éxito o lanza una excepción en caso de error.
        """
        cursorPython = None
        try:           
            # Crear el cursor
            cursorPython = connection.cursor()
            v_salida = cursorPython.var(int)  # Variable de salida opcional, si el procedimiento lo requiere
            # Parámetros que recibe el procedimiento almacenado
            params = [str(valorAnterior), str(valorNuevo), datetime.now(),v_salida]
            # Llamar al procedimiento almacenado
            cursorPython.callproc("insert_logData", params)
            print("Log insertado con éxito.")
        except Exception as e:
            # Captura de errores durante la ejecución del procedimiento
            print(f"Error al guardar log: {e}")
            raise
        finally:
            # Cerrar el cursor si fue creado
            if cursorPython:
                cursorPython.close()
