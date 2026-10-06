# Sistema de recepción de condominio

Programa desarrollado en Python para registrar ingresos y salidas de visitantes, consultar movimientos por departamento y proteger el DNI.

## Funcionalidades

- Registrar ingresos mediante tickets.
- Registrar salidas y observaciones.
- Consultar registros por ticket y departamento.
- Consultar el DNI mediante contraseña administrativa.
- Validar destinos correspondientes a cinco edificios y 80 departamentos.

## Instalación

Se requiere Python 3 y pip. Desde la carpeta del proyecto, ejecutar:

```powershell
python -m pip install -r requirements.txt
```

## Ejecución

```powershell
python main.py
```

El programa muestra un menú para realizar las operaciones. La contraseña administrativa de demostración es `admin123`.

## Pruebas automatizadas

Instalar las dependencias de desarrollo:

```powershell
python -m pip install -r requirements-dev.txt
```

Ejecutar las pruebas:

```powershell
python -m pytest tests -v
```

## Estructura del proyecto

```text
main.py
src/
├── controladores/
│   └── gestor_recepcion.py
├── modelos/
│   ├── persona.py
│   ├── departamento.py
│   └── registro_acceso.py
└── seguridad/
    └── encriptacion.py
tests/
└── test_recepcion.py
```

- **main.py:** muestra el menú, solicita datos y presenta resultados.
- **gestor_recepcion.py:** coordina ingresos, salidas y consultas. Aplica Singleton y Facade.
- **persona.py:** conserva el nombre completo, la huella del DNI y el DNI cifrado.
- **departamento.py:** valida el código del destino.
- **registro_acceso.py:** representa cada acceso, incluyendo horarios y observaciones.
- **encriptacion.py:** proporciona cifrado Fernet, huellas HMAC-SHA-256 y validación de la contraseña.
- **test_recepcion.py:** contiene las pruebas automatizadas.

## Limitaciones

Este proyecto es un prototipo académico. Los registros y las claves criptográficas permanecen en memoria y se pierden al cerrar el programa. La contraseña administrativa es fija para la demostración. No incluye base de datos ni cuentas individuales de usuario.