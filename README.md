# Administrador de boletos de eventos
Sistema para adminsitrar los boletos de eventos
Se pueden realizar las siguientes acciones:
- Crear un evento
- Actualizar un evento
- Eliminar un evento
- Listar los eventos
- Obtener la informacion de solo un evento
- Vender un boleto para un evento
- Canjear un boleto
- Reembolsar un boleto

## Tabla de Contenidos

- [Estructura del proyecto](#estructura-del-proyecto)
- [Despliegue](#despliegue)
- [Diagrama entidad relacion](#diagrama-entidad-relacion)
- [Diagrama de Base de datos](#diagrama-de-base-de-datos)
- [Como probar el servicio](#como-probar-el-servicio)
- [Ejemplos](#ejemplos)

## Estructura del proyecto

El proyecto está organizado de la siguiente manera:

- **ticket_manager/**: Contiene el código fuente del proyecto.
  - **ticket_manager/settings.py**: Contiene la configuracion de Django.
  - **ticket_manager/urls.py**: Definición de las rutas de la API.
  - **ticket_manager/schema.py**: Tipos y esquema necesarios para graphql.
  - **events/models.py**: Contiene los modelos necesarios.
  - **events/services.py**: Servicios que contienen la lógica de negocio.
  - **events/tests/**: Contiene las pruebas unitarias.
- **README.md**: Documentación del proyecto.
- **requirements.txt**: Contiene las dependencias del proyecto.
- **.gitignore**: Archivos y directorios que deben ser ignorados por Git.
- **Dockerfile**: Contiene la configuración de la imagen de Docker para el proyecto de Django.
- **docker-compose.yml**: Contiene la configuración de los servicios que se van a ejecutar para que la aplicación funcione correctamente.
- **start**: Script utilizado para iniciar el servidor Django.


Cada directorio y archivo tiene un propósito específico para mantener el código organizado y modular.

## Despliegue

Este proyecto se puede desplegar utilizando Docker y tambien en local

### Despliegue utilizando Docker
Puedes ejecutar la aplicación usando Docker Compose. Ejecuta:

```
docker-compose up
```

Esto levantará los servicios definidos en el archivo `docker-compose.yml`. La aplicación estará disponible en `http://localhost:8000`.

## Despliegue Local

Si prefieres ejecutar la aplicación de forma local, asegúrate de tener Python instalado y sigue estos pasos:

### 1. Crear un entorno virtual

Crea un entorno virtual en la raíz del proyecto:

```
python -m venv venv
```

### 2. Activar el entorno virtual

- En Windows:

```
venv\Scripts\activate
```

- En macOS y Linux:

```
source venv/bin/activate
```

### 3. Instalar los requisitos

Instala las dependencias necesarias utilizando el archivo `requirements.txt`:

```
pip install -r requirements.txt
```
### 4. Cambiar la configuración de la base de datos en `ticket_manager/settings.py`
Se debe crear una base de datos utilizando postgresql, y cambiar la configuración.

### 5. Aplicar las migraciones a la base de datos
Utilizar siguiente comando:
```
python manage.py migrate
```

### 6. Ejecutar la aplicación

Finalmente, ejecuta la aplicación con el comando:

```
python manage.py runserver
```

La aplicación estará disponible en `http://localhost:8000`.

## Diagrama entidad relacion

![diagra_er](https://github.com/user-attachments/assets/312245b7-9267-465f-bbe4-661648d3b2bb)

## Diagrama de Base de datos

![ticket_manager - public - events_event](https://github.com/user-attachments/assets/80e2f9c2-bc34-4353-b682-e06fa13e76a4)

## Como probar el servicio
La API desarrollada con Django y Graphql se puede probar de manera interactiva utilizando GraphiQL o Insomnia. Insomnia proporciona una interfaz visual que permite explorar y realizar solicitudes a los distintos querys y mutaciones.

Una vez desplegada la aplicación, GraphiQL estara disponible en `http://localhost:8000/graphql/`


## Ejemplos
Ejemplo sencillo para crear evento, listar eventos, consultar detalles de evento, vender boleto, revisar que el cambio se ve reflejado en los detalles del evento y regla de negocio de cantidad de boletos vendidos.

### Listar eventos
![image](https://github.com/user-attachments/assets/71fd81f7-6275-40ad-af61-1f73e7015391)
### Obtener evento con detalles de los boletos
![image](https://github.com/user-attachments/assets/74bc1a7c-30bc-4921-8568-b2dbabae4fc3)
### Crear evento
![image](https://github.com/user-attachments/assets/77b48419-b72b-4717-a42f-d30e4532841a)
### Actualizar evento
![image](https://github.com/user-attachments/assets/8f0356e4-7cda-4fd6-8976-3efe64631510)
### Eliminar evento
![image](https://github.com/user-attachments/assets/c4bb00d0-1f95-49c6-9919-29de0b787df2)
### Vender boleto
![image](https://github.com/user-attachments/assets/e8838cb3-1a80-444e-ace4-f87ea2adb06f)
### Canjear boleto
![image](https://github.com/user-attachments/assets/91186f90-6db6-4a8b-b337-ef5173a33927)
### Reembolsar boleto
![image](https://github.com/user-attachments/assets/ef44c4df-90ff-4ebd-82cb-9c720a1a5b15)

## Para revisar ejemplos más detallados donde se validan las reglas de negocio, consultar las pruebas unitarias.






