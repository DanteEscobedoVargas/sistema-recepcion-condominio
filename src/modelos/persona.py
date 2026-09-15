from abc import ABC, abstractmethod
from src.seguridad.encriptacion import EncriptadorSeguridad

class Persona(ABC):
    def __init__(self, id_persona: str, nombres: str, apellidos: str, dni: str):
        self._id_persona = id_persona
        self._nombres = nombres
        self._apellidos = apellidos
        # Encapsulamiento estricto: DNI encriptado en atributo privado
        self.__dni_encrip = EncriptadorSeguridad.hash_dni(dni)

    def get_nombre_completo(self) -> str:
        return f"{self._nombres} {self._apellidos}"

    def get_dni_encrip(self) -> str:
        return self.__dni_encrip

    @abstractmethod
    def validar_documento(self) -> bool:
        """Método abstracto que valida la integridad del documento en las subclases."""
        pass


class Residente(Persona):
    def __init__(self, id_persona: str, nombres: str, apellidos: str, dni: str, num_depa: str, es_propietario: bool):
        super().__init__(id_persona, nombres, apellidos, dni)
        self._num_depa = num_depa
        self._es_propietario = es_propietario

    def get_num_depa(self) -> str:
        return self._num_depa

    def validar_documento(self) -> bool:
        return len(self.get_dni_encrip()) == 64


class Visitante(Persona):
    def __init__(self, id_persona: str, nombres: str, apellidos: str, dni: str, parentesco_o_vinculo: str):
        super().__init__(id_persona, nombres, apellidos, dni)
        self._parentesco_o_vinculo = parentesco_o_vinculo

    def get_parentesco_o_vinculo(self) -> str:
        return self._parentesco_o_vinculo

    def validar_documento(self) -> bool:
        return len(self.get_dni_encrip()) == 64


class TrabajadorServicio(Persona):
    def __init__(self, id_persona: str, nombres: str, apellidos: str, dni: str, empresa_servicio: str):
        super().__init__(id_persona, nombres, apellidos, dni)
        self._empresa_servicio = empresa_servicio

    def get_empresa_servicio(self) -> str:
        return self._empresa_servicio

    def validar_documento(self) -> bool:
        return len(self.get_dni_encrip()) == 64