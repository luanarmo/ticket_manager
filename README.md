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

# Estructura del proyecto

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

# Despliegue

Este proyecto se puede desplegar utilizando Docker y tambien en local

## Despliegue utilizando Docker
Puedes ejecutar la aplicación usando Docker Compose. Ejecuta:

```
docker-compose up
```

Esto levantará los servicios definidos en el archivo `docker-compose.yml`. La aplicación estará disponible en `http://localhost:8000`.

## Despliegue Local

Si prefieres ejecutar la aplicación de forma local, asegúrate de tener Python instalado y sigue estos pasos:

# 1. Crear un entorno virtual

Crea un entorno virtual en la raíz del proyecto:

```
python -m venv venv
```

# 2. Activar el entorno virtual

- En Windows:

```
venv\Scripts\activate
```

- En macOS y Linux:

```
source venv/bin/activate
```

# 3. Instalar los requisitos

Instala las dependencias necesarias utilizando el archivo `requirements.txt`:

```
pip install -r requirements.txt
```
# 4. Cambiar la configuración de la base de datos en `ticket_manager/settings.py`
Se debe crear una base de datos utilizando postgresql, y cambiar la configuración.

# 5. Aplicar las migraciones a la base de datos
Utilizar siguiente comando:
```
python manage.py migrate
```

# 6. Ejecutar la aplicación

Finalmente, ejecuta la aplicación con el comando:

```
python manage.py runserver
```

La aplicación estará disponible en `http://localhost:8000`.

# Diagrama entidad relacion

![diagra_er](https://github.com/user-attachments/assets/312245b7-9267-465f-bbe4-661648d3b2bb)

# Diagrama de Base de datos

![ticket_manager - public - events_event](https://github.com/user-attachments/assets/80e2f9c2-bc34-4353-b682-e06fa13e76a4)

# Como probar el servicio
La API REST desarrollada con Django y Django REST Framework se puede probar de manera interactiva utilizando Swagger. Swagger proporciona una interfaz visual que permite explorar y realizar solicitudes a los distintos endpoints de la API sin necesidad de utilizar herramientas externas como Postman.

Una vez desplegada la aplicación, GraphiQL estara disponible en `http://localhost:8000/graphql/`


# Ejemplos
Ejemplo sencillo para crear evento, listar eventos, consultar detalles de evento, vender boleto, revisar que el cambio se ve reflejado en los detalles del evento y regla de negocio de cantidad de boletos vendidos.

## GraphiQL

# 🚧 Work in progress 🚧

Para consultar ejemplos más detallados, revisar las pruebas unitarias.






