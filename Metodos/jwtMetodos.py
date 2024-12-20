from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from Config.settingsConfig import settings

class jwtMetodos:
    # Instanciación del esquema de seguridad para el token
    security = HTTPBearer()
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
        """
        Genera un token JWT válido. Asegura que 'sub' esté presente en los datos.
        
        Parámetros:
            data (dict): Los datos que se incluyen en el payload del token (debe contener 'sub').
            expires_delta (timedelta): El tiempo de expiración del token (default: 1 hora).
            
        Retorna:
            str: El token JWT generado.
        """
        if "sub" not in data:
            raise ValueError("El payload debe contener el campo 'sub'")  # Verifica que el campo 'sub' esté presente
        
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta  # Define el tiempo de expiración
        to_encode.update({"exp": expire})  # Añade el campo de expiración al payload
        
        # Genera el token utilizando la clave secreta y el algoritmo de la configuración
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    @staticmethod
    def validate_token(credentials: HTTPAuthorizationCredentials = Security(security)):
        """
        Valida el token JWT extraído de los encabezados de la solicitud.
        
        Parámetros:
            credentials (HTTPAuthorizationCredentials): El token JWT recibido en el encabezado Authorization.
        
        Retorna:
            str: El identificador del usuario (usualmente el 'sub' del token).
        
        Lanza:
            HTTPException: Si el token no es válido o ha expirado.
        """
        token = credentials.credentials  # Extrae el token del encabezado Authorization
        
        try:
            # Decodifica el token usando la clave secreta y el algoritmo configurado
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            
            # Extrae el campo 'sub' que generalmente es el identificador del usuario
            user = payload.get("sub")
            if not user:
                # Si no se encuentra el campo 'sub', el token es inválido
                raise HTTPException(status_code=401, detail="Token inválido: falta el campo 'sub'")
            
            return user  # Devuelve el identificador del usuario (o cualquier campo relevante)
        
        except jwt.ExpiredSignatureError:
            # Si el token ha expirado, lanza una excepción HTTP
            raise HTTPException(status_code=401, detail="El token ha expirado")
        except jwt.InvalidTokenError:
            # Si el token es inválido por cualquier otra razón, lanza una excepción HTTP
            raise HTTPException(status_code=401, detail="Token inválido")
