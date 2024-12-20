from Clases.controlClass import ControlClass

class usuariosClass(ControlClass):
    def __init__(self, rut, nombre, apellido, estado, password_hash, password_plain=None, 
                 usuario_creacion=None, fecha_creacion=None, ip=None, 
                 usuario_modificacion=None, fecha_modificacion=None, 
                 id=None, existe=False):
        super().__init__(usuario_creacion, fecha_creacion, ip, usuario_modificacion, fecha_modificacion)
        
        self.rut = rut  # RUT del usuario
        self.nombre = nombre  # Nombre del usuario
        self.apellido = apellido  # Apellido del usuario
        self.estado = estado  # Estado del usuario
        self.password_hash = password_hash  # Contraseña cifrada       
        self.password_plain = password_plain # Contraseña en texto plano        
        self.id = id  # Identificador del usuario
        self.existe = existe  # Booleano que indica si el usuario existe en el sistema

    def __str__(self):
        return (
            f"RUT: {self.rut}, Nombre: {self.nombre} {self.apellido}, "
            f"Estado: {self.estado}, Existe: {'Sí' if self.existe else 'No'}, "
            f"Password (hash): {self.password_hash}"
        )