from typing import List
from src.modelos.persona import Persona
from src.modelos.departamento import RegistroAcceso

class GestorRecepcionController:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GestorRecepcionController, cls).__new__(cls)
            cls._instancia._historial_accesos = []
        return cls._instancia

    @classmethod
    def get_instancia(cls):
        return cls()

    def registrar_ingreso(self, persona: Persona, depa: str) -> RegistroAcceso:
        try:
            if not persona.validar_documento():
                raise ValueError("Error de validación en la identidad de la persona.")
            
            nuevo_id = f"REG-{len(self._historial_accesos) + 1:04d}"
            registro = RegistroAcceso(nuevo_id, persona, depa)
            self._historial_accesos.append(registro)
            return registro
        except Exception as e:
            print(f"[EXCEPCIÓN EN CONTROLADOR]: Error al registrar el ingreso -> {e}")
            raise

    # FUNCIÓN DE ORDEN SUPERIOR 1: filter() para consultar accesos por departamento
    def consultar_por_departamento(self, depa: str) -> List[RegistroAcceso]:
        return list(filter(lambda reg: reg.get_depa_destino() == depa, self._historial_accesos))

    # FUNCIÓN DE ORDEN SUPERIOR 2: map() para obtener los hashes de personas ingresadas
    def obtener_hashes_registrados(self) -> List[str]:
        return list(map(lambda reg: reg.get_persona().get_dni_encrip(), self._historial_accesos))