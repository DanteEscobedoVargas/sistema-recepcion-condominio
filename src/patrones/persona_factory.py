from src.modelos.persona import Persona, Residente, Visitante, TrabajadorServicio

class PersonaFactory:
    @staticmethod
    def crear_persona(tipo: str, id_p: str, nom: str, ape: str, dni: str, extra: str, es_prop: bool = False) -> Persona:
        tipo_clean = tipo.lower().strip()
        if tipo_clean == "residente":
            return Residente(id_p, nom, ape, dni, extra, es_prop)
        elif tipo_clean == "visitante":
            return Visitante(id_p, nom, ape, dni, extra)
        elif tipo_clean == "trabajador":
            return TrabajadorServicio(id_p, nom, ape, dni, extra)
        else:
            raise ValueError(f"Tipo de entidad '{tipo}' no soportado por la fábrica.")