from src.modelos.persona import Residente, Visitante, TrabajadorServicio

class PersonaFactory:
    @staticmethod
    def crear_persona(tipo, *args, **kwargs):
        tipo_clean = str(tipo).strip().lower()
        
        # Extraer parámetros
        nom = args[0] if len(args) > 0 else kwargs.get('nom', kwargs.get('nombre', ''))
        ape = args[1] if len(args) > 1 else kwargs.get('ape', kwargs.get('apellido', ''))
        dni = args[2] if len(args) > 2 else kwargs.get('dni', '')
        extra = args[3] if len(args) > 3 else kwargs.get('extra', '')

        # Si pasaron 3 argumentos posicionales
        if len(args) == 3:
            nom = args[0]
            ape = ""
            dni = args[1]
            extra = args[2]

        if tipo_clean in ["residente", "r"]:
            num_depa = extra
            es_propietario = True  # Pasa el 5° argumento obligatorio
            return Residente(nom, ape, dni, num_depa, es_propietario)

        elif tipo_clean in ["visitante", "v"]:
            try:
                return Visitante(nom, ape, dni, extra)
            except TypeError:
                return Visitante(nom, ape, dni)

        elif tipo_clean in ["servicio", "trabajadorservicio", "s"]:
            try:
                return TrabajadorServicio(nom, ape, dni, extra)
            except TypeError:
                return TrabajadorServicio(nom, ape, dni)

        else:
            raise ValueError(f"Tipo de persona no válido: '{tipo}'")