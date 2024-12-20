import subprocess
import sys

class pipConfig:

    lstPip =[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "pyjwt",
        "oracledb",
        "bcrypt",
        "httpx"
    ]
    @staticmethod
    def instalaDesinstalaPIP():
        try:
            """
            Actualiza PIP y Desinstala e instala paquetes usando pip desde la lista estática lstPip.
            """
            # Actualizar pip
            try:
                print("PIP: Actualizando pip...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
                print("PIP: pip actualizado correctamente.")
            except subprocess.CalledProcessError as e:
                print(f"PIP: Error al actualizar pip: {e}")

            for paquete in pipConfig.lstPip:
                # Desinstalar paquete
                try:
                    print(f"PIP: Desinstalando paquete: {paquete}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "-y", paquete])
                    print(f"PIP: Paquete desinstalado correctamente: {paquete}")
                except subprocess.CalledProcessError as e:
                    print(f"PIP: Error al desinstalar el paquete {paquete}: {e}")

                # Instalar paquete
                try:
                    print(f"PIP: Instalando paquete: {paquete}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])
                    print(f"PIP: Paquete instalado correctamente: {paquete}")
                except subprocess.CalledProcessError as e:
                    print(f"PIP: Error al instalar el paquete {paquete}: {e}")
        except Exception as e:
             raise Exception(f"PIP: Error -> {e}")

if __name__ == "__main__":
    print(f"\033[92mPIP: Proceso INICIADO\033[0m")
    pipConfig.instalaDesinstalaPIP()
    print(f"\033[92mPIP: Proceso TERMINADO exitosamente\033[0m")