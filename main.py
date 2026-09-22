from datetime import datetime
from src.patrones.persona_factory import PersonaFactory
from src.controladores.gestor_recepcion import GestorRecepcionController

def departamento_es_valido(depa: str) -> bool:
    """Valida que el departamento pertenezca a la torre (201, 202 ... 901, 902)"""
    if not depa.isdigit() or len(depa) != 3:
        return False
    piso = int(depa[0])
    num = depa[1:]
    return 2 <= piso <= 9 and num in ["01", "02"]

def mostrar_menu():
    print("\n" + "=" * 65)
    print("    SISTEMA DE CONTROL DE ACCESOS Y RECEPCIÓN DE CONDOMINIO")
    print("=" * 65)
    print("1. Registrar movimiento (Residente / Visitante / Servicio)")
    print("2. Registrar marca secundaria (Salida de visit. / Reingreso resid.)")
    print("3. Consultar accesos y horarios por Departamento")
    print("4. Ver hashes SHA-256 y consultar DNIs con contraseña (Ley N.° 29733)")
    print("5. Salir del sistema")
    print("=" * 65)

def ejecutar_sistema():
    gestor = GestorRecepcionController.get_instancia()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == "1":
            print("\n--- REGISTRO DE MOVIMIENTO ---")
            entrada_tipo = input("Tipo de persona (r: residente / v: visitante / s: servicio): ").strip().lower()
            
            if entrada_tipo in ["r", "residente"]:
                tipo = "residente"
            elif entrada_tipo in ["v", "visitante"]:
                tipo = "visitante"
            elif entrada_tipo in ["s", "servicio"]:
                tipo = "servicio"
            else:
                tipo = entrada_tipo

            nombre = input("Nombre completo: ").strip()

            if tipo == "residente":
                dni = "00000000"
                print("   [i] Identificación de residente validada automáticamente.")
            else:
                dni = input("Número de DNI (8 dígitos): ").strip()

            depa = input("Número de departamento (del 201/202 al 901/902): ").strip()
            while not departamento_es_valido(depa):
                print("   [!] Departamento no existe en la torre. Debe ser entre el 201, 202... hasta 901, 902.")
                depa = input("Reingrese departamento destino válido: ").strip()

            if tipo == "visitante":
                extra = input("Nombre de quien autoriza el ingreso: ").strip() or "N/A"
            elif tipo == "servicio":
                extra = input("Empresa o servicio (ej. Enel, Mantenimiento): ").strip() or "N/A"
            else:
                extra = depa

            try:
                partes = nombre.split(" ", 1)
                nom = partes[0]
                ape = partes[1] if len(partes) > 1 else ""

                persona = PersonaFactory.crear_persona(tipo, nom, ape, dni, extra)
                registro = gestor.registrar_ingreso(persona, depa)
                
                hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                if tipo == "residente":
                    setattr(registro, "hora_salida", hora_actual)
                    setattr(registro, "hora_ingreso", "EN EXTERIOR (FUERA)")
                    
                    print("\n[✔] ¡SALIDA DE RESIDENTE REGISTRADA!")
                    print(f" -> Ticket: {registro.get_id_registro()}")
                    print(f" -> Persona: {persona.get_nombre()} (RESIDENTE)")
                    print(f" -> Hora de Salida: {hora_actual}")
                    print(f" -> Departamento: Dpto {registro.get_depa_destino()}")
                else:
                    setattr(registro, "hora_ingreso", hora_actual)
                    setattr(registro, "hora_salida", "EN CONDOMINIO")

                    print("\n[✔] ¡INGRESO EXTERNO REGISTRADO!")
                    print(f" -> Ticket: {registro.get_id_registro()}")
                    print(f" -> Persona: {persona.get_nombre()} ({tipo.upper()})")
                    print(f" -> Hora de Ingreso: {hora_actual}")
                    print(f" -> DNI Encriptado (SHA-256): {persona.get_dni_encrip()}")
                    print(f" -> Destino: Dpto {registro.get_depa_destino()}")
            except Exception as e:
                print(f"\n[❌ ERROR AL REGISTRAR]: {e}")

        elif opcion == "2":
            print("\n--- MARCA COMPLEMENTARIA (SALIDA VISITANTES / RETORNO RESIDENTES) ---")
            ticket_buscar = input("Ingrese el Código de Ticket: ").strip()
            
            encontrado = False
            for reg in gestor._registros:
                if str(reg.get_id_registro()) == ticket_buscar or str(getattr(reg, "id_registro", "")) == ticket_buscar:
                    hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    es_residente = reg.get_persona().__class__.__name__ == "Residente"

                    if es_residente:
                        if getattr(reg, "hora_ingreso", "") != "EN EXTERIOR (FUERA)":
                            print(f"\n[!] El residente ya registró su retorno a las {getattr(reg, 'hora_ingreso')}.")
                        else:
                            setattr(reg, "hora_ingreso", hora_actual)
                            print(f"\n[✔] ¡RETORNO DE RESIDENTE REGISTRADO!")
                            print(f" -> Ticket: {ticket_buscar}")
                            print(f" -> Persona: {reg.get_persona().get_nombre()}")
                            print(f" -> Hora de Salida previa: {getattr(reg, 'hora_salida', 'N/A')}")
                            print(f" -> Hora de Retorno/Ingreso: {hora_actual}")
                    else:
                        if getattr(reg, "hora_salida", "") != "EN CONDOMINIO":
                            print(f"\n[!] La visita ya registró su salida a las {getattr(reg, 'hora_salida')}.")
                        else:
                            setattr(reg, "hora_salida", hora_actual)
                            print(f"\n[✔] ¡SALIDA DE VISITANTE REGISTRADA!")
                            print(f" -> Ticket: {ticket_buscar}")
                            print(f" -> Persona: {reg.get_persona().get_nombre()}")
                            print(f" -> Hora de Ingreso previa: {getattr(reg, 'hora_ingreso', 'N/A')}")
                            print(f" -> Hora de Salida: {hora_actual}")
                    
                    encontrado = True
                    break
            
            if not encontrado:
                print(f"\n[!] No se encontró ningún registro con el Ticket '{ticket_buscar}'.")

        elif opcion == "3":
            print("\n--- CONSULTA DE ACCESOS Y HORARIOS POR DEPARTAMENTO ---")
            depa_buscar = input("Ingrese el número de departamento a consultar: ").strip()
            if not departamento_es_valido(depa_buscar):
                print("   [!] El departamento ingresado no pertenece al condominio.")
                continue

            resultados = gestor.consultar_por_departamento(depa_buscar)
            if resultados:
                print(f"\n[+] Historial de accesos para el Dpto {depa_buscar}:")
                print("-" * 75)
                for reg in resultados:
                    h_in = getattr(reg, "hora_ingreso", "N/A")
                    h_out = getattr(reg, "hora_salida", "N/A")
                    print(f" Ticket: {reg.get_id_registro()} | {reg.get_persona().get_nombre()}")
                    print(f"    └─ HORA SALIDA: {h_out}  |  HORA INGRESO: {h_in}")
                    print("-" * 75)
            else:
                print(f"\n[!] No hay registros de ingreso para el departamento {depa_buscar}.")

        elif opcion == "4":
            print("\n--- CONSULTA DE REGISTROS SEGURIDAD Y DNI (LEY N.° 29733) ---")
            clave_ingresada = input("🔒 Ingrese la contraseña de administrador para ver los DNI: ").strip()
            
            try:
                registros = gestor.obtener_registros_protegidos(clave_ingresada)
                if registros:
                    print(f"\n[✔ ACCESO AUTORIZADO] Registros encriptados y protegidos ({len(registros)}):")
                    print("=" * 80)
                    for reg in registros:
                        p = reg.get_persona()
                        print(f" -> Ticket   : {reg.get_id_registro()}")
                        print(f" -> Nombre   : {p.get_nombre()}")
                        print(f" -> DNI Real : {p.get_dni_raw()}")
                        print(f" -> SHA-256  : {p.get_dni_encrip()}")
                        print("-" * 80)
                else:
                    print("\n[!] Aún no hay registros cargados en el sistema.")
            except PermissionError as err:
                print(f"\n[❌ ACCESO DENEGADO]: {err}")

        elif opcion == "5":
            print("\nCerrando el sistema de recepción... ¡Hasta luego!")
            break
        else:
            print("\n[!] Opción no válida. Por favor, marque entre 1 y 5.")

if __name__ == "__main__":
    ejecutar_sistema()