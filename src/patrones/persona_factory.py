from src.modelos.persona import Residente, Visitante, TrabajadorServicio, Repartidor, Persona

class PersonaFactory:
    @staticmethod
    def crear_persona(tipo: str, nom: str, ape: str, dni: str, extra: str = "") -> Persona:
        tipo_clean = str(tipo).strip().lower()

        if tipo_clean in ["residente", "r"]:
            return Residente(nombre=nom, apellido=ape, dni=dni, num_depa=extra, es_propietario=True)

        elif tipo_clean in ["visitante", "v"]:
            return Visitante(nombre=nom, apellido=ape, dni=dni, autoriza=extra)

        elif tipo_clean in ["servicio", "trabajadorservicio", "s"]:
            return TrabajadorServicio(nombre=nom, apellido=ape, dni=dni, empresa=extra)

        elif tipo_clean in ["repartidor", "delivery", "d"]:
            return Repartidor(nombre=nom, apellido=ape, dni=dni, empresa_delivery=extra)

        else:
            raise ValueError(f"Tipo de persona no válido: '{tipo}'")