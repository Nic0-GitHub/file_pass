# Gestor de Archivos con Flask

Este proyecto es una aplicación web simple desarrollada con Flask para gestionar archivos. Permite a los usuarios subir archivos al servidor, descargar archivos existentes y ver la lista de archivos disponibles.

## Características

- **Subida de Archivos:** Los usuarios pueden subir archivos al servidor, que se almacenarán en la carpeta de descargas.
- **Descarga de Archivos:** Los archivos almacenados en la carpeta de archivos pueden ser descargados por los usuarios.
- **Interfaz Web:** Utiliza Flask para generar una interfaz web donde los usuarios pueden interactuar con los archivos.

## Requisitos Previos

- Python 3.x
- Flask (`pip install Flask`)

## Estructura del Proyecto

project/
│
├── app.py # Archivo principal de la aplicación Flask
├── static/
│ ├── templates/ # Plantillas HTML
│ │ └── index.html # Plantilla principal para la interfaz de usuario
│ ├── css/
│ │ └── basics.css # Hoja de estilos CSS para la interfaz
│ └── js/
│ └── index.js # Archivo JavaScript para la interfaz interactiva
│
├── files/ # Carpeta donde se almacenan los archivos subidos
├── download/ # Carpeta donde se almacenan los archivos disponibles para descarga
└── logs/ # Carpeta donde se pueden almacenar registros de la aplicación


## Configuración

1. **Configuración de Directorios:**
   - La aplicación utiliza los siguientes directorios para almacenar archivos:
     - `files/`: Para almacenar archivos subidos por los usuarios.
     - `download/`: Para almacenar archivos disponibles para descarga.
     - `logs/`: Opcionalmente, para almacenar registros de la aplicación.

2. **Instalación de Dependencias:**
   - Instala Flask si aún no lo tienes instalado:
     ```
     pip install Flask
     ```

## Uso

1. **Ejecutar la Aplicación:**
   - Desde la línea de comandos, ejecuta el archivo `app.py` para iniciar el servidor Flask:
     ```
     python app.py <puerto> <modo_debug>
     ```
     - `<puerto>`: Puerto en el que se ejecutará la aplicación (por defecto 5000).
     - `<modo_debug>`: Modo de depuración (0 para desactivado, 1 para activado).

2. **Interactuar con la Aplicación:**
   - Abre un navegador web y accede a `http://localhost:<puerto>` para ver la interfaz de usuario.
   - Sube archivos utilizando el formulario provisto.
   - Descarga archivos haciendo clic en los enlaces de descarga disponibles.


## Créditos

Desarrollado por Nicolas Agustín Pieroni