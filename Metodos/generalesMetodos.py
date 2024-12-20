import bcrypt
import socket
import json
from datetime import datetime

class generalesMetodos:
    # Hashear la contraseña
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Genera un hash seguro para la contraseña.
        :param password: La contraseña en texto plano.
        :return: La contraseña hasheada.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Verificar la contraseña
    @staticmethod
    def verify_password(stored_hash: str, password: str) -> bool:
        """
        Verifica si una contraseña coincide con su hash almacenado.
        :param stored_hash: Hash de la contraseña almacenado.
        :param password: Contraseña en texto plano.
        :return: True si la contraseña coincide, False en caso contrario.
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        except Exception as e:
            print(f"Error al verificar la contraseña: {e}")
            raise
    
    # Obtener la IP de la máquina
    @staticmethod
    def getIP():
        """
        Devuelve la dirección IP de la máquina.
        :return: Dirección IP como string.
        """
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except Exception as e:         
            print(f"Error al obtener la IP: {e}")
            raise e

    # Verificar si una fecha es válida
    @staticmethod
    def es_fecha_valida(texto, formato='%d-%m-%Y'):
        """
        Verifica si una fecha tiene un formato válido.
        :param texto: Fecha en formato string.
        :param formato: Formato esperado de la fecha.
        :return: Objeto datetime si es válida, False si no lo es.
        """
        try:
            return datetime.strptime(texto, formato)
        except ValueError:
            return False

   # Convertir cualquier objeto a JSON
    @staticmethod
    def objeto_a_json(objeto):
        """
        Convierte cualquier objeto en una cadena JSON de forma dinámica.
        :param objeto: Objeto a convertir.
        :return: Cadena JSON formateada.
        """
        if isinstance(objeto, datetime):
            # Convierte datetime a ISO 8601
            return objeto.isoformat()
        elif hasattr(objeto, "__dict__"):
            # Convierte objetos a diccionarios recursivamente
            return {k: generalesMetodos.objeto_a_json(v) for k, v in objeto.__dict__.items()}
        elif isinstance(objeto, list):
            # Convierte cada elemento de la lista
            return [generalesMetodos.objeto_a_json(elem) for elem in objeto]
        elif isinstance(objeto, dict):
            # Convierte cada clave-valor en el diccionario
            return {k: generalesMetodos.objeto_a_json(v) for k, v in objeto.items()}
        else:
            # Retorna valores básicos directamente
            return objeto
 
    @staticmethod
    def objeto_a_json_string(objeto):
        """
        Convierte cualquier objeto en una cadena JSON formateada.
        :param objeto: Objeto a convertir.
        :return: Cadena JSON formateada.
        """
        return json.dumps(objeto)