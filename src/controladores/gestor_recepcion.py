from src.modelos.departamento import Departamento
from src.modelos.registro_acceso import RegistroAcceso
from src.seguridad.encriptacion import EncriptadorSeguridad
from src.modelos.persona import Persona
from copy import deepcopy


class GestorRecepcionController:
    """Singleton y Facade. Propietario de los registros originales de la sesión."""

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._registros = []
        return cls._instancia

    @classmethod
    def get_instancia(cls):
        return cls()

    def registrar_ingreso(self, nombres, apellidos, dni, destino, autoriza, observacion=""):
        persona = Persona(nombres, apellidos, dni)
        ticket = str(len(self._registros) + 1).zfill(3)
        registro = RegistroAcceso(ticket, persona, destino, autoriza, observacion)
        self._registros.append(registro)
        return deepcopy(registro)

    def registrar_salida(self, ticket, observacion=""):
        registro = self._buscar_registro(ticket)
        if registro is None:
            raise ValueError("No existe un registro con ese ticket.")
        registro.registrar_salida(observacion)
        return deepcopy(registro)

    def obtener_registros(self):
        # Entregar copias evita modificar los registros originales fuera del gestor.
        return deepcopy(self._registros)

    def buscar_por_ticket(self, ticket):
        registro = self._buscar_registro(ticket)
        return deepcopy(registro) if registro is not None else None

    def _buscar_registro(self, ticket):
        ticket = ticket.strip()
        if not ticket.isascii() or not ticket.isdigit() or int(ticket) < 1:
            raise ValueError("El ticket debe ser un número positivo, por ejemplo 001.")
        ticket = str(int(ticket)).zfill(3)
        for registro in self._registros:
            if registro.get_ticket() == ticket:
                return registro
        return None

    def consultar_por_departamento(self, destino):
        destino = Departamento.validar_codigo(destino)
        return deepcopy(list(filter(lambda r: r.get_destino() == destino, self._registros)))

    def contar_visitantes_en_condominio(self):
        return len(list(filter(lambda r: r.esta_activo(), self._registros)))

    def obtener_hashes_registrados(self, clave):
        if not EncriptadorSeguridad.validar_clave_acceso(clave):
            raise PermissionError("Contraseña incorrecta. Acceso denegado.")
        return list(map(lambda r: (r.get_ticket(), r.get_persona().get_dni_hash()), self._registros))

    def obtener_registros_protegidos(self, clave):
        if not EncriptadorSeguridad.validar_clave_acceso(clave):
            raise PermissionError("Contraseña incorrecta. Acceso denegado.")
        return self.obtener_registros()

    def consultar_dnis(self, clave):
        if not EncriptadorSeguridad.validar_clave_acceso(clave):
            raise PermissionError("Contraseña incorrecta. Acceso denegado.")
        return [
            (r.get_ticket(), r.get_persona().get_nombre(),
             r.get_persona().consultar_dni(clave), r.get_persona().get_dni_hash())
            for r in self._registros
        ]
