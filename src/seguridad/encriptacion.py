import hashlib
import hmac
import re
import secrets
from cryptography.fernet import Fernet, InvalidToken


class EncriptadorSeguridad:
    """Cifrado Fernet, huella del DNI y contraseña de consulta."""

    # Clave aleatoria por ejecución para dificultar probar todos los DNI posibles.
    _CLAVE_HASH = secrets.token_bytes(32)
    # Clave de cifrado aleatoria por sesión, independiente de admin123.
    _CIFRADOR = Fernet(Fernet.generate_key())

    @classmethod
    def hash_dni(cls, dni):
        if not re.fullmatch(r"[0-9]{8}", dni):
            raise ValueError("El DNI debe tener exactamente 8 dígitos del 0 al 9.")
        return hmac.new(cls._CLAVE_HASH, dni.encode("utf-8"), hashlib.sha256).hexdigest()

    # Contraseña fija para la demostración académica.
    _CLAVE_ADMIN = "admin123"

    @classmethod
    def validar_clave_acceso(cls, clave):
        return clave == cls._CLAVE_ADMIN

    @classmethod
    def cifrar_dni(cls, dni):
        if not re.fullmatch(r"[0-9]{8}", dni):
            raise ValueError("El DNI debe tener exactamente 8 dígitos del 0 al 9.")
        return cls._CIFRADOR.encrypt(dni.encode("utf-8"))

    @classmethod
    def descifrar_dni(cls, dni_cifrado, clave):
        if not cls.validar_clave_acceso(clave):
            raise PermissionError("Contraseña incorrecta. Acceso denegado.")
        try:
            return cls._CIFRADOR.decrypt(dni_cifrado).decode("utf-8")
        except InvalidToken as error:
            raise ValueError("No se pudo verificar el DNI cifrado.") from error
