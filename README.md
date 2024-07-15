# Lead Management System

## Descripción General

El objetivo de la solución es permitir la carga de usuarios “lead” al sistema, así como la posibilidad de recuperar sus datos y mostrarlos de forma apropiada, abarcando desde la captura de requerimientos hasta el despliegue, teniendo en cuenta requerimientos a futuro. Para ello, la solución será implementada en Python usando el framework FastAPI y el DBMS relacional MySQL, incluyendo el ORM SQLAlchemy para la interacción del backend con la base de datos.

## Propuesta de Solución

Consiste en la implementación de una API REST y 3 endpoints para las operaciones requeridas:
- **GET lead BY ID**
- **GET ALL leads**
- **POST lead**

En cuanto al diseño, se optó por implementar un patrón Repository para separar la lógica de negocio de la lógica de base de datos y facilitar la escalabilidad. Además, se tienen las operaciones de los endpoints por separado pensando en la escalabilidad, en caso de que a futuro se necesiten crear más endpoints de entidades diferentes.

Una cosa a recalcar es la característica de FastAPI de facilitar el uso de dependency injection, lo que me permitio crear una sesion de base de datos y cerrarla luego de usar la base de datos. El sistema de dependencias de FastAPI permite declarar dependencias usando funciones con 'yield'. Esto nos brinda disponibilidad de una sesión en cada request a un endpoint. Si bien es algo hecho por un tercero, esta característica fomenta la modularidad y facilita el testing.

## Diseño de la Base de Datos

Se consideró que un Lead puede estar cursando más de una carrera y que las materias son únicas de cada carrera.

![image](https://github.com/user-attachments/assets/81b739b3-686e-40d1-a8e7-c1283d3bc4ef)

## Approach

Siguiendo este diseño, el código sigue la siguiente lógica:

- **GET ALL leads**: Se hace una query de todos los registros de la tabla "leads" de la base de datos.
- **GET lead BY ID**: Se realiza una query en la tabla "leads" y devuelve el primer registro que coincide con la id provista. Si no lo encuentra, levanta una HTTPException.
- **POST lead**: Incluye la creación de otros objetos los cuales se agregan antes de confirmar la creación del registro "lead", en el siguiente orden (suponiendo que el nuevo lead está cursando una o más materias):
  1. Empieza la creación de un lead.
  2. Para cada cursado se empieza la creación de un cursado.
  3. Para cada cursado se crea una carrera (si ya existe, la devuelve).
  4. Para cada cursado se empieza la creación de una inscripción.
  5. Para cada inscripción se crea una materia (si ya existe, la devuelve).
  6. Se agregan las materias a cada inscripción y se crean las inscripciones.
  7. Se agregan las inscripciones a cada cursado y se crean los cursados.
  8. Se agregan los cursados al nuevo lead y se confirma la creación.

## No se Contempló:

- Testing
- Validación de casos particulares
- Manejo de errores y edge cases
- Diseño de un front end y la respectiva integración con el back end
- Despliegue en Docker

## Anexo

### Diagrama de Clases

![image](https://github.com/user-attachments/assets/a10ffe77-45b3-4e46-9f25-694822e845e8)

### Diagrama de Secuencia de la Creación de un Nuevo Lead Cursando Una o Más Carreras

![image](https://github.com/user-attachments/assets/c7caa952-3349-4d3f-b9c0-da77948e0319)
