# Taller de Sistemas Operativos - API de Imágenes (AWS Serverless)

Este repositorio contiene el código fuente, la configuración y los scripts para el desarrollo y despliegue de una API REST utilizando FastAPI. El proyecto cumple con los requerimientos del taller de Sistemas Operativos de la Universidad EIA, integrando almacenamiento en la nube, bases de datos relacionales y computación serverless.

## 🚀 Arquitectura y Tecnologías Utilizadas

* **Backend:** FastAPI (Python)
* **Adaptador Serverless:** Mangum
* **Almacenamiento de Archivos:** Amazon S3
* **Base de Datos Relacional:** Amazon RDS (MySQL)
* **Contenerización:** Docker
* **Registro de Contenedores:** Amazon ECR
* **Despliegue:** AWS Lambda (Function URL)

## ⚙️ Descripción de los Endpoints

### 1. Cargar Imagen (`POST /upload/`)
Permite a un usuario subir una imagen al sistema.
* **Parámetros:** `usuario` (texto) y `file` (archivo físico).
* **Validaciones:** Solo acepta formatos `image/png` y `image/jpeg`. Retorna error `415` si el formato es inválido.
* **Flujo:** Almacena la imagen en S3 bajo la ruta `usuario/nombre_archivo` y registra los metadatos (ID, usuario, ruta S3 y fecha de creación) en la base de datos RDS.

### 2. Obtener Imagen (`GET /imagen/`)
Consulta la ubicación y genera un acceso temporal a una imagen previamente subida.
* **Parámetros:** `usuario` y `nombre_imagen`.
* **Flujo:** Consulta la base de datos RDS para verificar la existencia. Si no existe, retorna un error `404`. Si existe, genera una URL prefirmada de Amazon S3 y la retorna junto con la fecha de almacenamiento.

## 💻 Instrucciones de Ejecución Local (Docker)

Para correr la aplicación de manera local, asegúrate de tener Docker instalado y las credenciales de AWS configuradas en tu entorno.

1. **Construir la imagen:**
````bash
   docker build -t app-fastapi-aws .
   ````

2. **Ejecutar el contenedor:**
````bash
   docker run -p 8080:8080 app-fastapi-aws
   ````

## ☁️ Despliegue en la Nube (AWS Lambda)

La aplicación ha sido empaquetada en una imagen de contenedor, publicada en Amazon ECR y desplegada a través de AWS Lambda. 

* **URL Pública de Invocación:** `https://ov47eba24dcsdnszje5c2qxdzy0delzn.lambda-url.us-east-2.on.aws/`

## 📁 Estructura del Proyecto

* `main.py`: Código principal de la aplicación FastAPI y conexión a AWS.
* `Dockerfile`: Instrucciones de contenerización basadas en la imagen oficial de AWS Lambda para Python.
* `requirements.txt`: Dependencias del proyecto.
* `README.md`: Documentación del proyecto.

*(Nota: Las evidencias y capturas de pantalla requeridas por el taller se encuentran anexadas en el documento de entrega principal).*
