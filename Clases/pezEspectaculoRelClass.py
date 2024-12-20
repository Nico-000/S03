from Clases.controlClass import ControlClass

class pezEspectaculoRelClass(ControlClass):
    def __init__(self, id_pez, id_espectaculo, fecha_participacion, 
                 usuario_creacion=None, fecha_creacion=None, 
                 ip=None, usuario_modificacion=None, fecha_modificacion=None, existe=False):
        super().__init__(usuario_creacion, fecha_creacion, ip, usuario_modificacion, fecha_modificacion, existe)
        self.id_pez = id_pez
        self.id_espectaculo = id_espectaculo
        self.fecha_participacion = fecha_participacion
    
    def __str__(self):
        return (
            f"ID Pez: {self.id_pez}, "
            f"ID Espectáculo: {self.id_espectaculo}, "
            f"Fecha Participación: {self.fecha_participacion}"
        )
