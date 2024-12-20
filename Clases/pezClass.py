from Clases.controlClass import ControlClass

class pezClass(ControlClass):
    def __init__(self, nombre_pez, especie_pez, edad_pez, 
                 usuario_creacion=None, fecha_creacion=None, ip=None, 
                 usuario_modificacion=None, fecha_modificacion=None, existe=False):
        super().__init__(usuario_creacion, fecha_creacion, ip, usuario_modificacion, fecha_modificacion, existe)
        self.nombre_pez = nombre_pez
        self.especie_pez = especie_pez
        self.edad_pez = edad_pez
    
    def __str__(self):
        return (
            f"Nombre Pez: {self.nombre_pez}, "
            f"Especie Pez: {self.especie_pez}, "
            f"Edad Pez: {self.edad_pez}"
        )
