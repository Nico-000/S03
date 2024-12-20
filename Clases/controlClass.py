class ControlClass:
    def __init__(self, usuario_creacion=None, fecha_creacion=None, ip=None, 
                 usuario_modificacion=None, fecha_modificacion=None, id=None, existe=False):
        self.usuario_creacion = usuario_creacion
        self.fecha_creacion = fecha_creacion 
        self.ip = ip
        self.usuario_modificacion = usuario_modificacion
        self.fecha_modificacion = fecha_modificacion
        self.id = id
        self.existe = existe

    def __str__(self):
        return (
            f"Usuario Creación: {self.usuario_creacion}", 
            f"Fecha Creación: {self.fecha_creacion}, "
            f"IP: {self.ip}, "
            f"Usuario Modificación: {self.usuario_modificacion}, "
            f"Fecha Modificación: {self.fecha_modificacion}, "
            f"ID: {self.id}, "
            f"Existe: {self.existe}"
        )
