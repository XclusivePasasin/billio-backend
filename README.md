# billio-backend
Billio: Sistema automatizado para gestionar, organizar y procesar facturas electrónicas recibidas por correo. Almacena, extrae información clave, y facilita la visualización y análisis financiero con una interfaz amigable.

# Instalación del Entorno Virtual y Dependencias

Sigue los siguientes pasos para configurar el entorno virtual y las dependencias de tu proyecto.

## 1. Instalar `virtualenv`

```bash
pip install virtualenv
```

## 2. Crear el Entorno Virtual

```bash
python -m venv venv
```

## 3. Configurar la Política de Ejecución (solo en Windows)

```bash
Set-ExecutionPolicy -Scope CurrentUser Unrestricted
```

## 4. Activar el Entorno Virtual

### En Windows:

```bash
venv\Scripts\activate
```

### En macOS/Linux:

```bash
source venv/bin/activate
```

## 5. Instalar las Dependencias

Una vez activado el entorno virtual, instala las dependencias del proyecto:

```bash
pip install -r requirements.txt
```

¡Y listo! Ahora tienes el entorno configurado y las dependencias instaladas.
