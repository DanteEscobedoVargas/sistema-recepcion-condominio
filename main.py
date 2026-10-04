from getpass import getpass
from src.controladores.gestor_recepcion import GestorRecepcionController


def mostrar_ticket(registro):
    print(f"\nTicket: #{registro.get_ticket()}")
    print(f"Persona: {registro.get_persona().get_nombre()}")
    print(f"Destino: {registro.get_destino()}")
    print(f"Autorizó: {registro.get_autoriza()}")
    print(f"Ingreso: {registro.get_hora_ingreso():%Y-%m-%d %H:%M:%S}")
    salida = registro.get_hora_salida()
    print("Salida:", salida.strftime("%Y-%m-%d %H:%M:%S") if salida else "En condominio")
    print("Observación de ingreso:", registro.get_observacion_ingreso() or "Sin observaciones")
    print("Observación de salida:", registro.get_observacion_salida() or "Sin observaciones")


def registrar_ingreso(gestor):
    print("\n--- REGISTRAR INGRESO ---")
    nombres = input("Nombres: ").strip()
    apellidos = input("Apellidos: ").strip()
    dni = getpass("DNI (8 dígitos; no se muestra al escribir): ").strip()
    destino = input("Torre y departamento de destino (ejemplo T2D502): ").strip()
    autoriza = input("¿Quién autorizó su ingreso?: ").strip()
    observacion = input("Observación de ingreso (opcional, Enter para omitir): ")
    registro = gestor.registrar_ingreso(nombres, apellidos, dni, destino, autoriza, observacion)
    print("Ingreso registrado correctamente.")
    mostrar_ticket(registro)


def registrar_salida(gestor):
    print("\n--- REGISTRAR SALIDA ---")
    ticket = input("Número de ticket (ejemplo 001): ")
    registro = gestor.buscar_por_ticket(ticket)
    if registro is None:
        raise ValueError("No existe un registro con ese ticket.")
    if not registro.esta_activo():
        raise ValueError("Este ticket ya tiene una salida registrada.")
    observacion = input("Observación de salida (opcional, Enter para omitir): ")
    registro = gestor.registrar_salida(ticket, observacion)
    print("Salida registrada correctamente.")
    mostrar_ticket(registro)


def visualizar_tickets(gestor):
    print("\na. Ver todos los tickets\nb. Buscar por número de ticket")
    opcion = input("Seleccione a/b: ").strip().lower()
    if opcion == "a":
        registros = gestor.obtener_registros()
        print(f"Total de tickets: {len(registros)}")
        print(f"Personas en condominio: {gestor.contar_visitantes_en_condominio()}")
        for registro in registros:
            mostrar_ticket(registro)
    elif opcion == "b":
        registro = gestor.buscar_por_ticket(input("Número de ticket: "))
        if registro is None:
            raise ValueError("No existe un registro con ese ticket.")
        mostrar_ticket(registro)
    else:
        raise ValueError("Seleccione a o b.")


def consultar_departamento(gestor):
    destino = input("Torre y departamento a consultar (ejemplo T1D201): ")
    registros = gestor.consultar_por_departamento(destino)
    if not registros:
        print("No hay registros para ese destino.")
    for registro in registros:
        mostrar_ticket(registro)


def consultar_seguridad(gestor):
    clave = getpass("Contraseña de administrador: ")
    datos = gestor.consultar_dnis(clave)
    if not datos:
        print("No hay registros.")
    for ticket, nombre, dni, dni_hash in datos:
        print(f"\nTicket: #{ticket} | Persona: {nombre}")
        print("DNI (consulta autorizada):", dni)
        print("Huella HMAC-SHA-256:", dni_hash)


def mostrar_menu():
    print("\n--- RECEPCIÓN DEL CONDOMINIO ---")
    print("1. Registrar ingreso")
    print("2. Registrar salida")
    print("3. Visualizar y buscar tickets de acceso")
    print("4. Consultar accesos y horarios por torre y departamento")
    print("5. Consultar DNI y huellas con contraseña")
    print("6. Salir del sistema")


def ejecutar_sistema():
    gestor = GestorRecepcionController.get_instancia()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ").strip()
        try:
            if opcion == "1":
                registrar_ingreso(gestor)
            elif opcion == "2":
                registrar_salida(gestor)
            elif opcion == "3":
                visualizar_tickets(gestor)
            elif opcion == "4":
                consultar_departamento(gestor)
            elif opcion == "5":
                consultar_seguridad(gestor)
            elif opcion == "6":
                print("Cerrando el sistema de recepción.")
                break
            else:
                print("Seleccione una opción del 1 al 6.")
        except (ValueError, PermissionError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    try:
        ejecutar_sistema()
    except (EOFError, KeyboardInterrupt):
        print("\nSistema cerrado.")
