# taskify-backend
Taskify es una plataforma de gestión de actividades que centraliza todas las tareas de un equipo. Facilita la asignación de tareas, el seguimiento de fechas límite, la colaboración en tiempo real y la organización de proyectos, desde los más simples hasta los más complejos, de forma intuitiva y eficiente.

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
