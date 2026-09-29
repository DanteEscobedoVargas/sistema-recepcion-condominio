from datetime import datetime
from src.patrones.persona_factory import PersonaFactory
from src.controladores.gestor_recepcion import GestorRecepcionController

def departamento_es_valido(depa: str) -> bool:
    if not depa.isdigit() or len(depa) != 3:
        return False
    piso = int(depa[0])
    num = depa[1:]
    return 2 <= piso <= 9 and num in ["01", "02"]

def mostrar_menu():
    print("\n" + "=" * 68)
    print("    SISTEMA DE CONTROL DE ACCESOS Y RECEPCIÓN DE CONDOMINIO")
    print("=" * 68)
    print("1. Registrar movimiento (Residente / Visitante / Servicio / Repartidor)")
    print("2. Registrar marca secundaria (Salida de visit. / Reingreso resid.)")
    print("3. Visualizar y buscar Tickets de Acceso (GENERAL / POR CÓDIGO)")
    print("4. Consultar accesos y horarios por Departamento")
    print("5. Ver hashes SHA-256 y consultar DNIs con contraseña (Ley N.° 29733)")
    print("6. Salir del sistema")
    print("=" * 68)

def ejecutar_sistema():
    gestor = GestorRecepcionController.get_instancia()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            print("\n--- REGISTRO DE MOVIMIENTO ---")
            entrada_tipo = input("Tipo de persona (r: residente / v: visitante / s: servicio / d: repartidor): ").strip().lower()
            
            if entrada_tipo in ["r", "residente"]:
                tipo = "residente"
            elif entrada_tipo in ["v", "visitante"]:
                tipo = "visitante"
            elif entrada_tipo in ["s", "servicio"]:
                tipo = "servicio"
            elif entrada_tipo in ["d", "repartidor", "delivery"]:
                tipo = "repartidor"
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
            elif tipo == "repartidor":
                extra = input("Empresa de delivery (ej. Rappi, PedidosYa): ").strip() or "N/A"
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
                    registro.set_hora_salida(hora_actual)
                    registro.set_hora_ingreso("EN EXTERIOR (FUERA)")
                    
                    print("\n[✔] ¡SALIDA DE RESIDENTE REGISTRADA!")
                    print(f" 🎫 TICKET GENERADO: #{registro.get_id_registro()}")
                    print(f" -> Persona: {persona.get_nombre()} (RESIDENTE)")
                    print(f" -> Hora de Salida: {hora_actual}")
                    print(f" -> Departamento: Dpto {registro.get_depa_destino()}")
                else:
                    registro.set_hora_ingreso(hora_actual)
                    registro.set_hora_salida("EN CONDOMINIO")

                    print("\n[✔] ¡INGRESO EXTERNO REGISTRADO!")
                    print(f" 🎫 TICKET GENERADO: #{registro.get_id_registro()}")
                    print(f" -> Persona: {persona.get_nombre()} ({tipo.upper()})")
                    print(f" -> Hora de Ingreso: {hora_actual}")
                    print(f" -> DNI Encriptado (SHA-256): {persona.get_dni_encrip()}")
                    print(f" -> Destino: Dpto {registro.get_depa_destino()}")
            except Exception as e:
                print(f"\n[❌ ERROR AL REGISTRAR]: {e}")

        elif opcion == "2":
            print("\n--- MARCA COMPLEMENTARIA (SALIDA VISITANTES / RETORNO RESIDENTES) ---")
            ticket_buscar = input("Ingrese el Código de Ticket (ej. 001): ").strip()
            
            reg = gestor.buscar_por_ticket(ticket_buscar)
            if reg:
                hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                es_residente = reg.get_persona().__class__.__name__ == "Residente"

                if es_residente:
                    if reg.get_hora_ingreso() != "EN EXTERIOR (FUERA)":
                        print(f"\n[!] El residente ya registró su retorno a las {reg.get_hora_ingreso()}.")
                    else:
                        reg.set_hora_ingreso(hora_actual)
                        print(f"\n[✔] ¡RETORNO DE RESIDENTE REGISTRADO!")
                        print(f" -> Ticket: #{reg.get_id_registro()}")
                        print(f" -> Persona: {reg.get_persona().get_nombre()}")
                        print(f" -> Hora de Salida previa: {reg.get_hora_salida()}")
                        print(f" -> Hora de Retorno/Ingreso: {hora_actual}")
                else:
                    if reg.get_hora_salida() != "EN CONDOMINIO":
                        print(f"\n[!] La visita ya registró su salida a las {reg.get_hora_salida()}.")
                    else:
                        reg.set_hora_salida(hora_actual)
                        print(f"\n[✔] ¡SALIDA DE VISITANTE REGISTRADA!")
                        print(f" -> Ticket: #{reg.get_id_registro()}")
                        print(f" -> Persona: {reg.get_persona().get_nombre()}")
                        print(f" -> Hora de Ingreso previa: {reg.get_hora_ingreso()}")
                        print(f" -> Hora de Salida: {hora_actual}")
            else:
                print(f"\n[!] No se encontró ningún registro con el Ticket '#{ticket_buscar.zfill(3)}'.")

        elif opcion == "3":
            print("\n--- VISUALIZADOR DE TICKETS GENERADOS ---")
            print("a. Ver listado general de todos los tickets")
            print("b. Buscar ticket específico por código")
            sub_opcion = input("Seleccione una opción (a/b): ").strip().lower()

            if sub_opcion == "a":
                registros = gestor.obtener_registros()
                if registros:
                    print(f"\n Total de tickets registrados: {len(registros)}")
                    print(f" Visitas activas en condominio: {gestor.contar_visitantes_en_condominio()}")
                    print("=" * 75)
                    for r in registros:
                        tipo_p = r.get_persona().__class__.__name__
                        print(f" 🎫 TICKET #{r.get_id_registro()} | Dpto: {r.get_depa_destino()} | {r.get_persona().get_nombre()} ({tipo_p})")
                        print(f"    ├─ Hora Ingreso: {r.get_hora_ingreso()}")
                        print(f"    └─ Hora Salida : {r.get_hora_salida()}")
                        print("-" * 75)
                else:
                    print("\n[!] No hay tickets generados en el sistema aún.")

            elif sub_opcion == "b":
                cod = input("Ingrese el número de ticket a buscar (ej. 001): ").strip()
                r = gestor.buscar_por_ticket(cod)
                if r:
                    print("\n" + "=" * 50)
                    print(f" DETALLE DEL TICKET #{r.get_id_registro()}")
                    print("=" * 50)
                    print(f" Persona  : {r.get_persona().get_nombre()}")
                    print(f" Tipo     : {r.get_persona().__class__.__name__}")
                    print(f" Destino  : Departamento {r.get_depa_destino()}")
                    print(f" Ingreso  : {r.get_hora_ingreso()}")
                    print(f" Salida   : {r.get_hora_salida()}")
                    print(f" Hash DNI : {r.get_persona().get_dni_encrip()[:16]}...")
                    print("=" * 50)
                else:
                    print(f"\n[!] El ticket #{cod.zfill(3)} no existe.")

        elif opcion == "4":
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
                    print(f" Ticket: #{reg.get_id_registro()} | {reg.get_persona().get_nombre()}")
                    print(f"    └─ HORA SALIDA: {reg.get_hora_salida()}  |  HORA INGRESO: {reg.get_hora_ingreso()}")
                    print("-" * 75)
            else:
                print(f"\n[!] No hay registros para el departamento {depa_buscar}.")

        elif opcion == "5":
            print("\n--- CONSULTA DE REGISTROS SEGURIDAD Y DNI (LEY N.° 29733) ---")
            clave_ingresada = input("🔒 Ingrese la contraseña de administrador para ver los DNI: ").strip()
            
            try:
                registros = gestor.obtener_registros_protegidos(clave_ingresada)
                if registros:
                    print(f"\n[✔ ACCESO AUTORIZADO] Registros encriptados y protegidos ({len(registros)}):")
                    print("=" * 80)
                    for reg in registros:
                        p = reg.get_persona()
                        print(f" -> Ticket   : #{reg.get_id_registro()}")
                        print(f" -> Nombre   : {p.get_nombre()}")
                        print(f" -> DNI Real : {p.get_dni_raw()}")
                        print(f" -> SHA-256  : {p.get_dni_encrip()}")
                        print("-" * 80)
                else:
                    print("\n[!] Aún no hay registros cargados en el sistema.")
            except PermissionError as err:
                print(f"\n[❌ ACCESO DENEGADO]: {err}")

        elif opcion == "6":
            print("\nCerrando el sistema de recepción... ¡Hasta luego!")
            break
        else:
            print("\n[!] Opción no válida. Por favor, marque entre 1 y 6.")

if __name__ == "__main__":
    ejecutar_sistema()