from datetime import datetime
from src.modelos.departamento import Departamento


class RegistroAcceso:
    """Un ticket conserva el ingreso y, posteriormente, su salida."""

    def __init__(self, ticket, persona, destino, autoriza, observacion=""):
        self._destino = Departamento.validar_codigo(destino)
        if not autoriza.strip():
            raise ValueError("Debe indicar quién autorizó el ingreso.")
        self._ticket = ticket
        self._persona = persona
        self._autoriza = autoriza.strip()
        self._hora_ingreso = datetime.now()
        self._hora_salida = None
        self._observacion_ingreso = observacion.strip()
        self._observacion_salida = ""

    def registrar_salida(self, observacion=""):
        if not self.esta_activo():
            raise ValueError("Este ticket ya tiene una salida registrada.")
        self._hora_salida = datetime.now()
        self._observacion_salida = observacion.strip()

    def esta_activo(self):
        return self._hora_salida is None

    def get_ticket(self):
        return self._ticket

    def get_persona(self):
        return self._persona

    def get_destino(self):
        return self._destino

    def get_autoriza(self):
        return self._autoriza

    def get_hora_ingreso(self):
        return self._hora_ingreso

    def get_hora_salida(self):
        return self._hora_salida

    def get_observacion_ingreso(self):
        return self._observacion_ingreso

    def get_observacion_salida(self):
        return self._observacion_salida
