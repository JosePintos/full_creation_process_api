![image](https://github.com/user-attachments/assets/5bd0cdf9-4bb2-428b-b655-74bb653d12c4)# register_leads
Descripción general: el objetivo de la solucion es permitir la carga de usuarios “lead” al sistema, así como la posibilidad de recuperar sus datos y mostrarlos de forma apropiada, abarcando desde la captura de requerimientos hasta el despliegue. Teniendo en cuenta requerimientos a futuro. Para ello la solucion sera implementada en Python usando el framework FastAPI y el DBMS relacional MySQL incluyendo el ORM SQLAlchemy para la interaccion del back con la base de datos.

Propuesta de solucion
Consiste en la implementacion de una API REST y 3 endopoints para las operaciones requeridas:
-GET lead BY ID
-GET ALL leads
-POST lead

En cuanto al diseño, se optó por implementar un patron Repository para separar la logica de negocio de la logica de base de datos y facilitar la escalabilidad. Ademas se tienen las operaciones de los endpoints por separado pensando en la escalabilidad, en caso de que a futuro se necesiten crear mas endpoints de entidades diferentes.
Una cosa a recalcar es la caracteristica de SQLAlchemy de facilitar el uso de dependency injection a la hora de crear y asignar una sesion de base de datos asegurando la disponibilidad de una sesion en cada request a un endpoint. Si bien es algo hecho por un tercero, esta caracteristica fomenta la modularidad y facilita el testing.

Diseño de la base datos:
Se consideró que un Lead puede estar cursando mas de una carrera y que las materias son unicas de cada carrera.
![image](https://github.com/user-attachments/assets/81b739b3-686e-40d1-a8e7-c1283d3bc4ef)

Approach
Siguiendo este diseño, el código sigue la siguiente logica:
-GET ALL leads: simplemente se hace una query de todos los registros de la tabla "leads" de la base de datos
-GET lead BY ID: se realiza una query en la tabla "leads" y devuelve el primer registro que coincide con la id provista, si no lo encuentra levanta una HTTPException
-POST lead: incluye la creacion de otros objetos los cuales se agregan antes de confirmar la creacion del registro "lead", en el siguiente orden (suponiendo que el nuevo lead esta cursando una o mas materias):
  1. Empieza la creacion de un lead
  2. Para cada cursado se empieza la creacion de un cursado
  3. Para cada cursado se crea una carrera (si ya existe, la devuelve)
  4. Para cada cursado se empieza la creacion de una inscripcion
  5. Para cada inscripcion se crea una materia (si ya existe, la devuelve)
  6. Se agregan las materias a cada inscripcion y se crean las inscripciones
  7. Se agregan las inscripciones a cada cursado y se crean los cursados
  8. Se agregan los cursados al nuevo lead y se confirma la creacion

No se contemplo:
-Testing
-Validacion de casos particulares
-Manejo de errores y edge cases
-Diseño de un front end y la respectiva integracion con el back end
-Despliegue en Docker

ANEXO
Diagrama de clases
![image](https://github.com/user-attachments/assets/a10ffe77-45b3-4e46-9f25-694822e845e8)

Diagrama de sequencia de la creacion de un nuevo lead cursando una o mas carreras:
![image](https://github.com/user-attachments/assets/c7caa952-3349-4d3f-b9c0-da77948e0319)

