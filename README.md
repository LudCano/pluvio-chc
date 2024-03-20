

# pluvio-chc
Análisis de datos de comparación entre el pluviómetro manual y automático en CHC (Chacaltaya). Desarrollado y mantenido por: Ludving Adolfo Cano [lcano@chacaltaya.edu.bo](mailto:lcano@chacaltaya.edu.bo) , Tahis Belen Peñaloza [tpenaloza@chacaltaya.edu.bo](mailto:tpenaloza@chacaltaya.edu.bo)
## Introduccion
- describes, dates,
- outputs f
- figures
- structure

## Descripcion de los datos 
Los datos fueron privada (automatic, manual repositorio observadores)
data set dates
variables

## Pre-procesamiento
-procesamiento archivo manual 
concatenamiento, uniformizacion
procesamiento de fechas
-procesamiento archivo autoomatico

- archivo observadores


## Procesamiento

### 1. Obteniendo eventos manuales
correlacion entre las tablas manual y automatico
ajustes
calculo de la direfencia de las medidas tomadas manual y automaticamente
ademas de la medidas tomadas por observador

### 2. Eventos perdidos
obtenemos los datos perdidos del automatico que no fueron registrados
precip > 0
horas perdidas que no se anotaron por el observador, duracion del evento
### 3. Tabla final
 completando datode la tabla general
- manual (proc) automatic (auto) observadores (observers) perdidos (perdidos)
eventos no registrados
data > manual >fecha	h0	hf	pluvio	observador	fechahora	duracion
       auto>fecha,hora,precip,fechahora
 
### 4. Acumulados
obtenemos los datos del automatico que no han sido registrados 


## Productos
### 1. Todos los eventos (`outputs/all_events.csv`)
Tabla resumida de todos los eventos, cuenta con columnas

 - **fecha**: Fecha
 - **fechahora**: Fecha y hora de inicio de evento
 - **duracion**: Duración de evento (en horas, incluye la hora inicial)
 - **pluvio**: Medida en mm manual
 - **precip**: Medida en mm automatico
 - **observador**: Observador del día de inicio (nota: tomar esto en cuenta en eventos de duración de más de un día).
 - **tipo**: Tipo de evento, toma los valores:
  - `0`: Evento marcado por el observador (pluvio > 0)
  - `1`: Evento _perdido_ (precip > 0 y pluvio = 0)
  - `2`: Evento no registrado (precip = pluvio = 0)

## Resultados
#

![](figs/comparison_events.png)
Primera comparación entre la duración de eventos, los mm marcados por los observadores y los mm por el automático.
