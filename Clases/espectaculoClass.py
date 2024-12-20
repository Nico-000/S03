from Clases.controlClass import ControlClass

class espectaculoClass(ControlClass):
    def __init__(self, nombre_espectaculo, duracion, descripcion, 
                 usuario_creacion=None, fecha_creacion=None, ip=None, 
                 usuario_modificacion=None, fecha_modificacion=None, existe=False):
        super().__init__(usuario_creacion, fecha_creacion, ip, usuario_modificacion, fecha_modificacion, existe)
        self.nombre_espectaculo = nombre_espectaculo
        self.duracion = duracion
        self.descripcion = descripcion
    
    def __str__(self):
        return (
            f"Nombre Espectáculo: {self.nombre_espectaculo}, "
            f"Duración: {self.duracion}, "
            f"Descripción: {self.descripcion}"
        )
