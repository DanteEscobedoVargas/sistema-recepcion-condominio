import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import main
from src.modelos.persona import Persona
from src.modelos.departamento import Departamento
from src.controladores.gestor_recepcion import GestorRecepcionController


class PruebasRecepcion(unittest.TestCase):
    def setUp(self):
        GestorRecepcionController._instancia = None
        self.gestor = GestorRecepcionController.get_instancia()

    def ingreso(self, destino="T2D502", observacion="Entrega de paquete"):
        return self.gestor.registrar_ingreso("Nombre", "Ficticio", "12345678", destino, "Autorizante ficticio", observacion)

    def test_todos_los_destinos(self):
        codigos = [f"T{torre}D{piso}0{depa}" for torre in range(1, 6)
                   for piso in range(2, 10) for depa in (1, 2)]
        self.assertEqual(len(codigos), 80)
        for codigo in codigos:
            self.assertEqual(Departamento.validar_codigo(codigo), codigo)
        self.assertEqual(Departamento.validar_codigo(" t2d502 "), "T2D502")

    def test_destinos_invalidos(self):
        for codigo in ("T0D201", "T6D201", "T1D101", "T1D1001", "T2D503", "201", "T1D²01"):
            with self.subTest(codigo=codigo), self.assertRaises(ValueError):
                self.ingreso(codigo)
        self.assertEqual(self.gestor.obtener_registros(), [])

    def test_datos_obligatorios(self):
        for nombres, apellidos, dni in (("", "Apellido", "12345678"),
                                        ("Nombre", "", "12345678"),
                                        ("Nombre", "Apellido", "123"),
                                        ("Nombre", "Apellido", "abcdefgh")):
            with self.assertRaises(ValueError):
                Persona(nombres, apellidos, dni)
        with self.assertRaises(ValueError):
            self.gestor.registrar_ingreso("Nombre", "Ficticio", "12345678", "T1D201", "")

    def test_salida_y_observaciones(self):
        registro = self.ingreso()
        self.assertEqual(self.gestor.contar_visitantes_en_condominio(), 1)
        registro = self.gestor.registrar_salida("1", "Se retiró con el paquete")
        self.assertEqual(registro.get_observacion_ingreso(), "Entrega de paquete")
        self.assertEqual(registro.get_observacion_salida(), "Se retiró con el paquete")
        self.assertGreaterEqual(registro.get_hora_salida(), registro.get_hora_ingreso())
        self.assertEqual(self.gestor.contar_visitantes_en_condominio(), 0)
        with self.assertRaises(ValueError):
            self.gestor.registrar_salida("001", "No debe sobrescribir")
        self.assertEqual(registro.get_observacion_salida(), "Se retiró con el paquete")

    def test_ticket_inexistente_e_invalido(self):
        self.assertIsNone(self.gestor.buscar_por_ticket("999"))
        for ticket in ("", "abc", "0", "²"):
            with self.assertRaises(ValueError):
                self.gestor.buscar_por_ticket(ticket)
        with self.assertRaises(ValueError):
            self.gestor.registrar_salida("999")

    def test_consultas_separan_torres_y_no_exponen_lista(self):
        primero = self.ingreso("T1D201")
        segundo = self.ingreso("T2D201")
        self.assertEqual([r.get_ticket() for r in self.gestor.consultar_por_departamento("T1D201")], [primero.get_ticket()])
        self.assertEqual([r.get_ticket() for r in self.gestor.consultar_por_departamento("T2D201")], [segundo.get_ticket()])
        self.gestor.obtener_registros().clear()
        self.assertEqual(len(self.gestor.obtener_registros()), 2)
        self.assertEqual(len(self.gestor.obtener_hashes_registrados("admin123")), 2)

    def test_singleton(self):
        self.ingreso()
        self.assertIs(self.gestor, GestorRecepcionController())
        self.assertEqual(len(GestorRecepcionController().obtener_registros()), 1)

    def test_consulta_huellas_con_clave(self):
        self.ingreso()
        with self.assertRaises(PermissionError):
            self.gestor.obtener_hashes_registrados("incorrecta")
        huellas = self.gestor.obtener_hashes_registrados("admin123")
        self.assertEqual(huellas[0][0], "001")
        self.assertEqual(len(huellas[0][1]), 64)

    def test_persona_no_conserva_dni_original(self):
        persona = Persona("Nombre", "Ficticio", "12345678")
        self.assertNotIn("12345678", vars(persona).values())
        self.assertNotIn("_dni", vars(persona))
        self.assertIsInstance(persona._dni_cifrado, bytes)
        self.assertNotIn(b"12345678", persona._dni_cifrado)

    def test_consultas_no_modifican_originales(self):
        creado = self.ingreso()
        creado.registrar_salida("Cambio externo")
        self.assertTrue(self.gestor.buscar_por_ticket("1").esta_activo())
        listado = self.gestor.obtener_registros()
        listado[0].registrar_salida("Otra copia")
        self.assertTrue(self.gestor.buscar_por_ticket("1").esta_activo())
        self.gestor.registrar_salida("1", "Salida oficial")
        self.assertFalse(self.gestor.buscar_por_ticket("1").esta_activo())

    def test_descifrado_requiere_clave_y_respeta_cambios(self):
        from src.seguridad.encriptacion import EncriptadorSeguridad
        persona = Persona("Nombre", "Ficticio", "12345678")
        with self.assertRaises(PermissionError):
            persona.consultar_dni("incorrecta")
        self.assertEqual(persona.consultar_dni("admin123"), "12345678")
        with patch.object(EncriptadorSeguridad, "_CLAVE_ADMIN", "otra-clave"):
            with self.assertRaises(PermissionError):
                persona.consultar_dni("admin123")
            self.assertEqual(persona.consultar_dni("otra-clave"), "12345678")

    def test_cifrado_alterado_se_rechaza(self):
        persona = Persona("Nombre", "Ficticio", "12345678")
        persona._dni_cifrado = b"datos-alterados"
        with self.assertRaises(ValueError):
            persona.consultar_dni("admin123")

    def test_consulta_normal_no_muestra_dni(self):
        registro = self.ingreso()
        salida = io.StringIO()
        with redirect_stdout(salida):
            main.mostrar_ticket(registro)
        self.assertNotIn("12345678", salida.getvalue())
        with self.assertRaises(PermissionError):
            self.gestor.consultar_dnis("incorrecta")
        self.assertEqual(self.gestor.consultar_dnis("admin123")[0][2], "12345678")

    def test_menu_completo(self):
        entradas = ["1", "Nombre", "Ficticio", "T2D502", "Autorizante",
                    "Observación ingreso", "3", "a", "3", "b", "1", "4", "T2D502",
                    "2", "001", "Observación salida", "2", "001", "5", "6"]
        salida = io.StringIO()
        with patch("builtins.input", side_effect=entradas), patch("main.getpass", side_effect=["12345678", "admin123"]), \
             redirect_stdout(salida):
            main.ejecutar_sistema()
        texto = salida.getvalue()
        self.assertIn("Ingreso registrado correctamente", texto)
        self.assertIn("Salida registrada correctamente", texto)
        self.assertIn("ya tiene una salida", texto)
        self.assertIn("Observación ingreso", texto)
        self.assertIn("Observación salida", texto)
        self.assertIn("DNI (consulta autorizada): 12345678", texto)
        self.assertIn("HMAC-SHA-256", texto)
        self.assertEqual(self.gestor.contar_visitantes_en_condominio(), 0)


if __name__ == "__main__":
    unittest.main()
