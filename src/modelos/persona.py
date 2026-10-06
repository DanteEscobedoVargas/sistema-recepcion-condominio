from src.seguridad.encriptacion import EncriptadorSeguridad


class Persona:
    """Un único modelo para las personas que ingresan al condominio."""

    def __init__(self, nombres: str, apellidos: str, dni: str):
        self.set_nombre(nombres, apellidos)
        self._dni_hash = EncriptadorSeguridad.hash_dni(dni)
        self._dni_cifrado = EncriptadorSeguridad.cifrar_dni(dni)

    def get_nombre(self):
        return self._nombre

    def set_nombre(self, nombres: str, apellidos: str) -> None:
        """Valida y actualiza el nombre completo."""
        if not isinstance(nombres, str) or not isinstance(apellidos, str):
            raise ValueError("Los nombres y apellidos deben ser texto.")

        nombres = nombres.strip()
        apellidos = apellidos.strip()

        if not nombres or not apellidos:
            raise ValueError("Los nombres y apellidos son obligatorios.")

        self._nombre = f"{nombres} {apellidos}"

    def get_dni_hash(self):
        return self._dni_hash

    def consultar_dni(self, clave):
        """Descifra solo para una consulta autorizada; no conserva el resultado."""
        return EncriptadorSeguridad.descifrar_dni(self._dni_cifrado, clave)
    
