import hashlib

class EncriptadorSeguridad:
    """Clase encargada del tratamiento seguro de datos personales (Ley N.° 29733)."""
    
    # Contraseña maestra para desencriptar o consultar DNIs en el sistema
    _CLAVE_ADMIN = "admin123"

    @staticmethod
    def hash_dni(dni: str) -> str:
        """Aplica hashing SHA-256 para no almacenar datos sensibles en texto plano."""
        if not dni or len(dni) < 6:
            raise ValueError("El documento de identidad debe contener al menos 6 caracteres válidos.")
        return hashlib.sha256(dni.encode('utf-8')).hexdigest()

    @classmethod
    def validar_clave_acceso(cls, clave_ingresada: str) -> bool:
        """Valida si la contraseña ingresada por el usuario es correcta."""
        return clave_ingresada.strip() == cls._CLAVE_ADMIN