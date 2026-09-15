from datetime import datetime
from typing import List, Optional
from src.modelos.persona import Persona, Residente

class Departamento:
    def __init__(self, numero_departamento: str, piso: int):
        self._numero_departamento = numero_departamento
        self._piso = piso
        self._residentes: List[Residente] = []

    def agregar_residente(self, residente: Residente) -> None:
        self._residentes.append(residente)

    def obtener_residentes(self) -> List[Residente]:
        return self._residentes


class RegistroAcceso:
    def __init__(self, id_registro: str, persona: Persona, depa_destino: str):
        self._id_registro = id_registro
        self._persona = persona
        self._depa_destino = depa_destino
        self._fecha_ingreso = datetime.now()
        self._fecha_salida: Optional[datetime] = None

    def marcar_salida(self) -> None:
        self._fecha_salida = datetime.now()

    def get_id_registro(self) -> str:
        return self._id_registro

    def get_depa_destino(self) -> str:
        return self._depa_destino

    def get_persona(self) -> Persona:
        return self._persona