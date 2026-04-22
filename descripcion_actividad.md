# Ejercicio 1: Sistema Integral de Gestión de Clientes, Servicios y Reservas

## Descripción general

En un equipo conformado por **cinco (5) estudiantes**, deberán desarrollar un sistema integral orientado a objetos, **sin uso de bases de datos**, capaz de gestionar clientes, servicios y reservas para una empresa llamada **Software FJ**, que ofrece los siguientes tipos de servicios:

- Reservas de salas
- Alquiler de equipos
- Asesorías especializadas

El objetivo de esta tarea es construir una aplicación **estable, modular y extensible** que implemente de forma rigurosa los principios de la programación orientada a objetos y el manejo avanzado de excepciones, garantizando que el sistema siga funcionando aun cuando se presenten errores durante su ejecución.

---

## Restricciones técnicas

- **No se permite** el uso de ningún motor o sistema de base de datos.
- Toda la gestión de información debe realizarse mediante **objetos, listas y estructuras en memoria**.
- El uso de archivos está **permitido únicamente** para el registro de eventos y errores (logs).

---

## Requisitos del sistema

### Principios de diseño

El sistema debe demostrar un diseño orientado a objetos completamente funcional, aplicando de manera rigurosa los siguientes principios:

| Principio | Descripción |
|---|---|
| Abstracción | Uso de clases abstractas para representar entidades generales del sistema |
| Encapsulación | Protección y validación de datos personales e internos |
| Herencia | Clases derivadas que extienden comportamiento de clases base |
| Polimorfismo | Métodos sobrescritos con comportamientos específicos por clase |
| Manejo de excepciones | Control robusto, personalizado y encadenado de errores |

---

### Arquitectura de clases

El sistema debe incluir, como mínimo, las siguientes clases y componentes:

#### Clase abstracta base
Una clase abstracta que represente las entidades generales del sistema, sirviendo como fundamento para el resto de la jerarquía de clases.

#### Clase `Cliente`
- Validaciones robustas sobre los datos de entrada.
- Encapsulación estricta de los datos personales.

#### Clase abstracta `Servicio` y servicios especializados
- Una clase abstracta `Servicio` como base común.
- **Al menos tres (3)** clases de servicios especializados que hereden de `Servicio`.
- Cada servicio especializado debe implementar:
  - Métodos sobrescritos para **calcular costos**.
  - Métodos sobrescritos para **describir el servicio**.
  - Métodos sobrescritos para **validar parámetros**.

#### Clase `Reserva`
Debe integrar los siguientes elementos:
- Cliente asociado
- Servicio seleccionado
- Duración de la reserva
- Estado de la reserva

E implementar las operaciones de:
- **Confirmación** de reserva
- **Cancelación** de reserva
- **Procesamiento** de reserva

Todas con manejo de excepciones incorporado.

#### Métodos sobrecargados
El sistema debe incluir métodos con diferentes variantes de invocación, por ejemplo:
- Cálculo de costos con impuestos.
- Cálculo de costos con descuentos.
- Cálculo de costos con parámetros opcionales.

#### Archivo de logs
Un archivo de registro donde se almacenen **todos los errores y eventos relevantes** del sistema durante su ejecución.

---

## Manejo de excepciones

El sistema deberá incorporar un manejo robusto y completo de excepciones. Los requerimientos mínimos son:

### Tipos de bloques requeridos

- `try / except`
- `try / except / else`
- `try / except / finally`
- Encadenamiento de excepciones

### Excepciones personalizadas

El sistema debe definir y utilizar **excepciones personalizadas** para cubrir situaciones específicas del dominio de negocio.

### Situaciones de error que el sistema debe manejar

El sistema debe ser capaz de detectar, registrar y recuperarse ante las siguientes situaciones, entre otras:

- Datos de entrada inválidos
- Parámetros faltantes o incompletos
- Operaciones no permitidas
- Intentos de reserva incorrectos
- Servicios no disponibles
- Cálculos inconsistentes
- Cualquier otra situación que comprometa la operación normal de la aplicación

> Cada error detectado debe quedar registrado en el archivo de logs. La aplicación debe **mantenerse activa y estable** en todo momento, independientemente de los errores que ocurran.

---

## Simulación de operaciones

El sistema debe simular **al menos 10 operaciones completas**, que incluyan obligatoriamente:

- Registros **válidos** de clientes.
- Registros **inválidos** de clientes.
- Creación **correcta** de servicios.
- Creación **incorrecta** de servicios.
- Reservas **exitosas**.
- Reservas **fallidas**.

Estas operaciones deben demostrar la capacidad del programa para **continuar funcionando ante errores graves** y manejar excepciones de manera controlada y profesional.

---

## Entregable

El equipo debe entregar **un único proyecto** que cumpla con los siguientes criterios:

- Completamente funcional y ejecutable sin interrupciones.
- Organizado y estructurado de forma clara y coherente.
- Debidamente documentado (clases, métodos y lógica principal).
- Que demuestre la correcta aplicación de la **programación orientada a objetos** y el **manejo avanzado de excepciones** en un entorno sin base de datos.