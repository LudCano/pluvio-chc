# CODIGO DE PROCESAMIENTO DATOS MANUALES
# L. Cano



def proc_manual():
        
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
    dff2 = dff.copy()
    dff.columns = ["fecha", "h0", "hf", "pluvio", "observador"] #renombrando columnas a nombres mas cortos
    dff2.columns = ["fecha", "h0", "hf", "pluvio", "observador"] #renombrando columnas a nombres mas cortos

    # -------------------
    ## ELIMINACION DE NANS
    # Solo importan los eventos, entonces borramos los nans
    len0 = len(dff)
    dff.dropna(inplace=True)
    #print("Se borraron", len0-len(dff), "lineas")
    #print("Quedan", len(dff), "eventos de lluvia")

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


    ## CREANDO ARCHIVO DE SOLO OBSERVADORES POR DIA
    # util para acumulados
    # asumiendo que en los casos que la lluvia 
    dff2 = dff2[["fecha", "observador"]]
    observadores = []; fechas = []; bandera = []
    for i in dff2.fecha.unique():
        aux = dff2[dff2.fecha == i]
        if len(aux) > 1:
            if len(aux.observador.unique()) > 1:
                flg = 1
            else:
                flg = 0
        else:
            flg = 0
        obs = aux.observador.to_list()[0]
        fechas.append(i)
        observadores.append(obs)
        bandera.append(flg)

    df3 = pd.DataFrame(list(zip(fechas, observadores, bandera)), columns = ["fecha", "observador", "mult_obs"])
    df3.to_csv("outputs/observador_por_dia.csv", index = False)
    return

def proc_automatic():
    ## PROCESAMIENTO DE ARCHIVO AUTOMATICO
    fname = "data/Chacaltaya_hr_form_v13.dat"
    output = "data/automatico.csv"


    # LIBRERIAS
    import pandas as pd


    ## LEYENDO DATOS
    d = pd.read_csv(fname, sep = " ")
    d = d[["DATE_LOCAL", "TIME_LOCAL", "Precip_Tot"]] #obteniendo columnas relevantes
    d.columns = ["fecha", "hora", "precip"]
    d["fechahora"] = pd.to_datetime(d.fecha +" "+ d.hora)
    # guardando archivo
    d.to_csv(output, index = False)
    return



def proc_conico():
    ## PROCESAMIENTO DE DATOS DEL CÓNICO
    fname = 'data/conic_pluvio_CHC_by_event.xlsx'
    output = 'data/conico.csv'

    # Librerias
    import pandas as pd
    import datetime as dt

    # Lectura de datos
    d = pd.read_excel(fname, sheet_name=None)

    lst_sheets = []

    for i in range(2021,2025):
        aux = d[str(i)].copy()
        lst_sheets.append(aux)

    dff = pd.concat(lst_sheets, axis = 0)
    dff.dropna(subset = ['HH_start'], inplace = True)
    datestimes = []; precips = []
    for i, j, k, l, p in zip(dff.YYYY_start, dff.MM_start, dff.DD_start, dff.HH_start,
                             dff.Precip_amount_mm):
        dd = dt.datetime(year = i, month=int(j), day=int(k), hour=int(l))
        datestimes.append(dd)
        precips.append(p)

    df_conic = pd.DataFrame(list(zip(datestimes, precips)), columns=['fechahora', 'conico'])
    manual = pd.read_csv('data/manual.csv')
    manual['fechahora'] = pd.to_datetime(manual.fechahora)
    
    juntos = pd.merge(manual, df_conic, how = 'left', on = 'fechahora')
    juntos.to_csv('data/manual.csv', index = False)

if __name__ == "__main__":
    proc_conico()