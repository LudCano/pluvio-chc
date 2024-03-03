# CODIGO DE PROCESAMIENTO DATOS MANUALES
# L. Cano


# Librerias
import pandas as pd
import datetime as dt


# Ruta de datos
datos_manuales = "data/PluvioCHC_por_evento.xlsx"

# Lectura de datos
d = pd.read_excel(datos_manuales, sheet_name = None)

# El parametro sheet_name = None nos devuelve todas las hojas del Excel
# como un diccionario, entonces podemos acceder a alguna con d["2024"]
#print(d.keys())

## CONCATENANDO TODAS LAS TABLAS
# Uniremos todas las hojas en una sola, obteniendo sólo las columnas que
# nos importan
lst_dfs = []

## PROCESAMIENTO DATOS MANUALES 2015-2024

#print(d["2021"].head()) #ejemplo pre-procesamiento
for i in range(2015,2025): #el limite sup es exclusivo
    aux = d[str(i)].copy()
    if i < 2022:
        ## Entre el 2015 y 2021 años la fila 2 tiene parte del encabezado, ahora se elimina
        ## y uniformiza
        aux.drop(0, axis=0, inplace = True)
    aux = aux[["FECHA", "DURACION_DEL_EVENTO", "Unnamed: 2", 
               "PLUVIO_2_CILINDRO_mm", "OBSERVADOR"]] # columnas importantes
    lst_dfs.append(aux)
    
dff = pd.concat(lst_dfs, axis=0)
dff.columns = ["fecha", "h0", "hf", "pluvio", "observador"] #renombrando columnas a nombres mas cortos
# -------------------
## ELIMINACION DE NANS
# Solo importan los eventos, entonces borramos los nans
len0 = len(dff)
dff.dropna(inplace=True)
print("Se borraron", len0-len(dff), "lineas")
print("Quedan", len(dff), "eventos de lluvia")

# -------------------
## PROCESAMIENTO DE FECHAS
# Ahora que tenemos una tabla unica, se hará una columna que será la fecha y hora inicial
# en formato que Python pueda leerlo, para eso se usará la librería datetime
def parse_especial(x, h2):
    """
    Crea el evento datetime si el evento de lluvia empezó el día anterior

    """
    l = x.split("_") #separamos para obtener la hora y el dia
    h = int(l[0]) #la hora inicial
    dia = int(l[1][:2])
    mes = int(l[1][2:4])
    anho = int(l[1][4:])
    dh = int((24-h) + h2) #delta tiempo en horas
    dat = dt.datetime(anho, mes, dia, h)
    return dat, dh


def parse_normal(d, h0, hf):
    de = d + dt.timedelta(hours = h0)
    dh = int(hf) - int(h0)
    return de, dh

fechas = dff["fecha"].to_list()
hora0 = dff["h0"].to_list()
horaf = dff["hf"].to_list()

dt0 = []
deltat = []
for f, h0, hf in zip(fechas, hora0, horaf):
    # corriendo en las 3 listas a la vez
    if type(h0) != str:
        # Caso en que no necesitamos el parse especial
        dtt, dh = parse_normal(f, h0, hf)
    else:
        # Caso de parse especial
        dtt, dh = parse_especial(h0, hf)
    dt0.append(dtt)
    deltat.append(dh)      

dff["fechahora"] = dt0 #añadiendo nueva columna
dff["duracion"] = deltat #igual
dff.to_csv("data/manual.csv", index = False) #guardando archivo