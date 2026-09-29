from typing import List
from src.modelos.persona import Residente

class Departamento:
    def __init__(self, numero_departamento: str, piso: int):
        self._numero_departamento = numero_departamento
        self._piso = piso
        self._residentes: List[Residente] = []

    def agregar_residente(self, residente: Residente) -> None:
        self._residentes.append(residente)

    def obtener_residentes(self) -> List[Residente]:
        return self._residentes

    def get_numero(self) -> str:
        return self._numero_departamento