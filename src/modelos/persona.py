from abc import ABC, abstractmethod
import hashlib

class Persona(ABC):
    def __init__(self, nombre, apellido="", dni=""):
        self._nombre = nombre
        self._apellido = apellido
        self._dni_encrip = self._encriptar_dni(dni)
        self._dni_raw = str(dni)

    def _encriptar_dni(self, dni):
        return hashlib.sha256(str(dni).encode('utf-8')).hexdigest()

    def validar_documento(self) -> bool:
        """Valida que el DNI tenga exactamente 8 dígitos numéricos según norma nacional."""
        return len(self._dni_raw) == 8 and self._dni_raw.isdigit()

    def get_nombre(self):
        return f"{self._nombre} {self._apellido}".strip()

    def get_dni_encrip(self):
        return self._dni_encrip

    def get_dni_raw(self):
        """Retorna el DNI original en texto plano para consultas autorizadas."""
        return self._dni_raw

class Residente(Persona):
    def __init__(self, nombre, apellido="", dni="", num_depa="", es_propietario=True, *args, **kwargs):
        super().__init__(nombre, apellido, dni)
        self._num_depa = num_depa
        self._es_propietario = es_propietario

class Visitante(Persona):
    def __init__(self, nombre, apellido="", dni="", autoriza="", *args, **kwargs):
        super().__init__(nombre, apellido, dni)
        self._autoriza = autoriza

class TrabajadorServicio(Persona):
    def __init__(self, nombre, apellido="", dni="", empresa="", *args, **kwargs):
        super().__init__(nombre, apellido, dni)
        self._empresa = empresa