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


# Proceso de solución

El primer paso fue leer detenidamente la prueba técnica para identificar los elementos clave: eventos y boletos, así como su relación en el sistema. A continuación, determiné la información que necesitaba almacenar para cada elemento, incluyendo nombres, fechas, entre otros.

Con esta información, creé un diagrama entidad-relación para visualizar cómo serían las tablas y los campos en la base de datos SQL, así como las relaciones entre eventos y boletos.

Una vez finalizado el diagrama, comencé el desarrollo. Cree una carpeta llamada "ticket_manager" y dentro de ella, establecí un entorno virtual. Luego, activé el entorno virtual e instalé las dependencias necesarias.

Con la estructura del proyecto lista, desarrollé los modelos basándome en el diagrama entidad-relación. Tras completar los modelos, creé los serializadores e implementé las validaciones correspondientes para cada campo. A continuación, desarrollé los viewsets para manejar las peticiones, comenzando por los servicios que definían las reglas de negocio.

Una vez terminados los servicios, definí el comportamiento de cada acción en los viewsets y agregué las rutas necesarias en la configuración del proyecto.

Después de implementar la funcionalidad, instalé las dependencias requeridas para las pruebas unitarias, apliqué las configuraciones necesarias y desarrollé las pruebas basadas en las reglas de negocio descritas en la prueba técnica. Por cada prueba unitaria que desarrollaba, la ejecutaba para asegurar su correcto funcionamiento.

Durante el proceso de pruebas, identifiqué y corregí varios errores en los servicios y serializadores. Tras completar todas las pruebas unitarias y comprobar que las reglas de negocio se aplicaban correctamente, instalé las dependencias y configuré Swagger para poder utilizar y probar los endpoints.

Al probar los endpoints con Swagger, encontré un error específico que resolví y, como resultado, también modifiqué las pruebas unitarias correspondientes.

Una vez que todo funcionó correctamente, consulté algunos proyectos previos para revisar la configuración de Docker y el archivo docker-compose.yml. Implementé Docker y realicé las modificaciones necesarias en el docker-compose.yml. Finalmente, probé el despliegue utilizando Docker Compose y todo funcionó como se esperaba.

# Cosas que agregue
Agregue algunas reglas de negocio para la accion de vender boletos que no se definieron en la prueba tecnica y ademas agregue una accion adicional "el reembolso del boleto" y tambien defini ciertas reglas de negocio que crei necesarias.

# Estructura del proyecto

El proyecto está organizado de la siguiente manera:

- **ticket_manager/**: Contiene el código fuente del proyecto.
  - **ticket_manager/settings.py**: Contiene la configuracion de Django.
  - **ticket_manager/urls.py**: Definición de las rutas de la API.
  - **events/models.py**: Contiene los modelos necesarios.
  - **events/serializers.py**: Contiene los serializadores que se utilizan para la validación de los datos de entrada y salida de la API.
  - **events/views.py**: Contiene los viewsets de la aplicación.
  - **events/routes.py**: Contiene la configuración de las rutas de la aplicacion 'events'.
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

# Diagrama de Base de datos

# Como probar el servicio
La API REST desarrollada con Django y Django REST Framework se puede probar de manera interactiva utilizando Swagger. Swagger proporciona una interfaz visual que permite explorar y realizar solicitudes a los distintos endpoints de la API sin necesidad de utilizar herramientas externas como Postman.

Una vez desplegada la aplicación, swagger estara disponible en `http://localhost:8000/swagger/`

Una vez en la interfaz de Swagger, verás una lista de todos los endpoints disponibles. Cada uno incluirá información sobre los métodos HTTP soportados (GET, POST, PUT, DELETE) y los parámetros necesarios.

Para realizar pruebas, simplemente selecciona el endpoint que deseas probar, haz cick en el botón "Try it out",completa los parámetros requeridos (si los hay) y haz clic en el botón "Execute". Swagger mostrará la respuesta de la API en tiempo real.

# Ejemplos