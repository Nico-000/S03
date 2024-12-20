from fastapi import FastAPI
from Config.logMiddlewareConfig import logMiddlewareConfig
from Routes.loginRoute import login_router
from Routes.userRoute import user_router
from Routes.dummyRoute import dummy_router
from Routes.apisRoute import apis_router
from Routes.pezRoute import pez_router
from Routes.espectaculoRoute import espectaculo_router
import uvicorn

# Crear la aplicación
app = FastAPI(
    title="API con JWT",
    description="API simple con autenticación JWT usando FastAPI",
    version="1.1.0"
)

# Instanciar la clase de middleware
log_middleware = logMiddlewareConfig()

# Registrar el middleware
@app.middleware("http")
async def log_requests_middleware(request, call_next):
    return await log_middleware.log_requests(request, call_next)

# Registrar routers
app.include_router(login_router)
app.include_router(user_router)
app.include_router(dummy_router)
app.include_router(apis_router)
app.include_router(pez_router)
app.include_router(espectaculo_router)
app.include_router(pezEspectaculoRel_router)
if __name__ == "__main__":
    puerto = 8081
    print(f"\033[93mhttp://localhost:{puerto}/docs\033[0m")
    uvicorn.run(app, host="localhost", port=puerto)