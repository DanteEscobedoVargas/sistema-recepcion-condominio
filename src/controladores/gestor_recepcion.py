from src.seguridad.encriptacion import EncriptadorSeguridad

class GestorRecepcionController:
    _instancia = None

    def __init__(self):
        if hasattr(self, "_inicializado") and self._inicializado:
            return
        self._registros = []
        self._inicializado = True

    @classmethod
    def get_instancia(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def registrar_ingreso(self, persona, depa):
        if hasattr(persona, "validar_documento") and not persona.validar_documento():
            raise ValueError("El documento (DNI) de la persona no es válido (debe tener 8 dígitos).")

        registro = RegistroAcceso(persona, depa)
        self._registros.append(registro)
        return registro

    def obtener_registros(self):
        """Método público para ver los registros sin errores de encapsulación."""
        return self._registros

    def consultar_por_departamento(self, depa):
        return list(filter(lambda r: str(r.get_depa_destino()) == str(depa), self._registros))

    def obtener_hashes_registrados(self):
        return list(map(lambda r: r.get_persona().get_dni_encrip(), self._registros))

    def obtener_registros_protegidos(self, clave_ingresada: str):
        """Devuelve los datos sensibles (DNI) únicamente si la clave es correcta."""
        if not EncriptadorSeguridad.validar_clave_acceso(clave_ingresada):
            raise PermissionError("Contraseña de administrador incorrecta. Acceso denegado.")
        return self._registros


class RegistroAcceso:
    _contador_id = 1

    def __init__(self, persona, depa_destino):
        self._id_registro = str(RegistroAcceso._contador_id).zfill(3)
        RegistroAcceso._contador_id += 1
        self._persona = persona
        self._depa_destino = depa_destino

    def get_id_registro(self):
        return self._id_registro

    def get_persona(self):
        return self._persona

    def get_depa_destino(self):
        return self._depa_destino