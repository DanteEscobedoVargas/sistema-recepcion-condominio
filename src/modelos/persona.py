from src.seguridad.encriptacion import EncriptadorSeguridad


class Persona:
    """Un único modelo para las personas que ingresan al condominio."""

    def __init__(self, nombres: str, apellidos: str, dni: str):
        if not nombres.strip() or not apellidos.strip():
            raise ValueError("Los nombres y apellidos son obligatorios.")
        self._nombre = f"{nombres.strip()} {apellidos.strip()}"
        self._dni_hash = EncriptadorSeguridad.hash_dni(dni)
        self._dni_cifrado = EncriptadorSeguridad.cifrar_dni(dni)

    def get_nombre(self):
        return self._nombre

    def get_dni_hash(self):
        return self._dni_hash

    def consultar_dni(self, clave):
        """Descifra solo para una consulta autorizada; no conserva el resultado."""
        return EncriptadorSeguridad.descifrar_dni(self._dni_cifrado, clave)
