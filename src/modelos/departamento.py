import re


class Departamento:
    """Cinco torres, pisos 2 al 9 y dos departamentos por piso."""

    @staticmethod
    def validar_codigo(codigo: str) -> str:
        codigo = codigo.strip().upper()
        if not re.fullmatch(r"T[1-5]D[2-9]0[12]", codigo):
            raise ValueError("Destino inválido. Ejemplo: T2D502. Torres 1-5, pisos 2-9, departamentos 01 o 02.")
        return codigo
