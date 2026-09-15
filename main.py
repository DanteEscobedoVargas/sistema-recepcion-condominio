from src.patrones.persona_factory import PersonaFactory
from src.controladores.gestor_recepcion import GestorRecepcionController

def main():
    print("==========================================================")
    print(" SISTEMA DE CONTROL DE ACCESOS Y RECEPCIÓN DE CONDOMINIO")
    print("==========================================================")
    
    controlador = GestorRecepcionController.get_instancia()

    try:
        # 1. Instanciación mediante el patrón Factory Method
        r1 = PersonaFactory.crear_persona("residente", "P-01", "Carlos", "Mendoza", "74859612", "101", True)
        v1 = PersonaFactory.crear_persona("visitante", "P-02", "Ana", "Torres", "12345678", "Prima")
        t1 = PersonaFactory.crear_persona("trabajador", "P-03", "Luis", "Gómez", "87654321", "Servicios SAC")

        # 2. Registro de accesos
        controlador.registrar_ingreso(r1, "101")
        controlador.registrar_ingreso(v1, "101")
        controlador.registrar_ingreso(t1, "202")

        # 3. Aplicación de Función de Orden Superior: filter()
        print("\n[+] Historial de accesos al Dpto 101 (filtrado con filter):")
        accesos_101 = controlador.consultar_por_departamento("101")
        for reg in accesos_101:
            p = reg.get_persona()
            print(f" -> ID: {reg.get_id_registro()} | Persona: {p.get_nombre_completo()} | Hash: {p.get_dni_encrip()[:16]}...")

        # 4. Aplicación de Función de Orden Superior: map()
        print("\n[+] Mapeo de hashes de seguridad de los accesos (map):")
        hashes = controlador.obtener_hashes_registrados()
        for h in hashes:
            print(f" -> SHA-256 Hash: {h[:24]}...")

    except Exception as err:
        print(f"\nExcepción capturada en la ejecución del sistema: {err}")

if __name__ == "__main__":
    main()