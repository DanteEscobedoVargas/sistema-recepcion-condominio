from datetime import datetime
from functools import reduce
from src.seguridad.encriptacion import EncriptadorSeguridad

class RegistroAcceso:
    _contador_id = 1

    def __init__(self, persona, depa_destino):
        self._id_registro = str(RegistroAcceso._contador_id).zfill(3)
        RegistroAcceso._contador_id += 1
        self._persona = persona
        self._depa_destino = depa_destino
        self._hora_ingreso = "N/A"
        self._hora_salida = "N/A"

    def get_id_registro(self) -> str:
        return self._id_registro

    def get_persona(self):
        return self._persona

    def get_depa_destino(self) -> str:
        return self._depa_destino

    def get_hora_ingreso(self) -> str:
        return self._hora_ingreso

    def set_hora_ingreso(self, hora: str):
        self._hora_ingreso = hora

    def get_hora_salida(self) -> str:
        return self._hora_salida

    def set_hora_salida(self, hora: str):
        self._hora_salida = hora


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
        return self._registros

    def buscar_por_ticket(self, ticket_id: str):
        """Busca un ticket específico en el sistema por su ID (ej. 001)."""
        resultados = list(filter(lambda r: r.get_id_registro() == ticket_id.zfill(3), self._registros))
        return resultados[0] if resultados else None

    def consultar_por_departamento(self, depa):
        return list(filter(lambda r: str(r.get_depa_destino()) == str(depa), self._registros))

    def obtener_hashes_registrados(self):
        return list(map(lambda r: r.get_persona().get_dni_encrip(), self._registros))

    def contar_visitantes_en_condominio(self) -> int:
        """Uso explícito de reduce() para sumar las visitas actualmente en el edificio."""
        return reduce(
            lambda acc, r: acc + (1 if r.get_hora_salida() == "EN CONDOMINIO" else 0),
            self._registros,
            0
        )

    def obtener_registros_protegidos(self, clave_ingresada: str):
        if not EncriptadorSeguridad.validar_clave_acceso(clave_ingresada):
            raise PermissionError("Contraseña de administrador incorrecta. Acceso denegado.")
        return self._registros