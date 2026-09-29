from abc import ABC, abstractmethod
import hashlib

class Persona(ABC):
    def __init__(self, nombre: str, apellido: str = "", dni: str = ""):
        self._nombre = nombre
        self._apellido = apellido
        self._dni_raw = str(dni)
        self._dni_encrip = self._encriptar_dni(dni)

    def _encriptar_dni(self, dni) -> str:
        return hashlib.sha256(str(dni).encode('utf-8')).hexdigest()

    def validar_documento(self) -> bool:
        """Valida que el DNI tenga exactamente 8 dígitos numéricos."""
        return len(self._dni_raw) == 8 and self._dni_raw.isdigit()

    def get_nombre(self) -> str:
        return f"{self._nombre} {self._apellido}".strip()

    def get_dni_encrip(self) -> str:
        return self._dni_encrip

    def get_dni_raw(self) -> str:
        """Retorna el DNI en texto plano para consultas autorizadas."""
        return self._dni_raw


class Residente(Persona):
    def __init__(self, nombre: str, apellido: str = "", dni: str = "", num_depa: str = "", es_propietario: bool = True):
        super().__init__(nombre, apellido, dni)
        self._num_depa = num_depa
        self._es_propietario = es_propietario


class Visitante(Persona):
    def __init__(self, nombre: str, apellido: str = "", dni: str = "", autoriza: str = ""):
        super().__init__(nombre, apellido, dni)
        self._autoriza = autoriza


class TrabajadorServicio(Persona):
    def __init__(self, nombre: str, apellido: str = "", dni: str = "", empresa: str = ""):
        super().__init__(nombre, apellido, dni)
        self._empresa = empresa


class Repartidor(Persona):
    def __init__(self, nombre: str, apellido: str = "", dni: str = "", empresa_delivery: str = ""):
        super().__init__(nombre, apellido, dni)
        self._empresa_delivery = empresa_delivery