import time
from fastapi import Request
import logging

class logMiddlewareConfig:
    """
    Middleware personalizado para registrar solicitudes HTTP.
    """
    def __init__(self):
        # Configurar el logger
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.logger = logging.getLogger("RequestLogger")

    async def log_requests(self, request: Request, call_next):
        """
        Middleware para registrar solicitudes HTTP.
        """
        start_time = time.time()  # Tiempo de inicio
        self.logger.info(f"Solicitud entrante: {request.method} {request.url}")

        # Registrar cabeceras útiles para depuración (opcional)
        if "Authorization" in request.headers:
            self.logger.debug(f"Token: {request.headers['Authorization']}")

        response = await call_next(request)  # Procesar la solicitud
        process_time = time.time() - start_time  # Tiempo de procesamiento
        self.logger.info(f"Solicitud completada: {response.status_code} en {process_time:.2f} seg")
        return response
