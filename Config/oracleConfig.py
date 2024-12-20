import oracledb
class oracleConfig:
    
    @staticmethod
    def connect():
        """Inicializa las  variables de entorno y configurando Oracle."""
        user = "nicolasJosemaria"
        password = "TurboSnail888$"
        host = "adb.sa-santiago-1.oraclecloud.com" 
        service_name = "ga97df7c3802ff4_shared202402_high.adb.oraclecloud.com"
        port = 1522
        """Establece y retorna una conexión a la base de datos Oracle."""
        try:
            # Crear el DSN manualmente con formato correcto
            dsn = (
                "(DESCRIPTION="
                "(ADDRESS=(PROTOCOL=tcps)(HOST={host})(PORT={port}))"
                "(CONNECT_DATA=(SERVICE_NAME={service_name}))"
                "(SECURITY=(SSL_SERVER_CERT_DN_MATCH=yes))"
                ")"
            ).format(host=host, port=port, service_name=service_name)

            connection = oracledb.connect(user=user, password=password, dsn=dsn)
            print(f"\tConexión exitosa a la base de datos.")
            return connection
        except oracledb.DatabaseError as e:
            raise

    @staticmethod
    def create_ref_cursor(cursor):
        """
        Crea una variable de tipo SYS_REFCURSOR usando el cursor proporcionado.
        :param cursor: Cursor activo asociado a una conexión.
        :return: Variable de tipo SYS_REFCURSOR.
        """
        return cursor.var(oracledb.CURSOR)