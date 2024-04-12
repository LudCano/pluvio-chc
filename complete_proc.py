"""
COMPLETADO DE DATOS EN TABLA GENERAL
L.Cano

El objetivo de este modulo es completar la tabla para todos los eventos
incluyendo los perdidos.
"""
def complete_table(date_start, date_fin):
    import pandas as pd
    import datetime as dt
    import numpy as np
    proc_fname = "outputs/processed.csv"
    auto_fname = "data/automatico.csv"
    observers_fname = "outputs/observador_por_dia.csv"
    perdidos_fname = "outputs/eventos_perdidos.csv"
    

    manual   = pd.read_csv(proc_fname)      #eventos ya procesados manuales
    auto     = pd.read_csv(auto_fname)      #datos pre-procesados automaticos
    obs_only = pd.read_csv(observers_fname) #solo observadores (para completar)
    perdidos = pd.read_csv(perdidos_fname)  #eventos perdidos
    # CORTANDO LAS MATRICES POR FECHA INICIAL Y FINAL
    def trim_df(d, d0, df):
        d0 = dt.datetime.strptime(d0, "%Y-%m-%d")
        df = dt.datetime.strptime(df, "%Y-%m-%d")
        df = df + dt.timedelta(hours = 24)
        d["fechahora"] = pd.to_datetime(d.fechahora)
        d2 = d.loc[(d.fechahora >= d0) & (d.fechahora < df)]
        return d2

    manual = trim_df(manual, date_start, date_fin)
    auto = trim_df(auto, date_start, date_fin)
    perdidos = trim_df(perdidos, date_start, date_fin)
    obs_only["fechahora"] = pd.to_datetime(obs_only.fecha)
    obs_only = trim_df(obs_only, date_start, date_fin)

    # DE UNA FORMA PARECIDA A LOS EVENTOS PERDIDOS, QUITAMOS PRIMERO LOS EVENTOS YA MARCADOS
    def create_dts(start, duration):
        dts = []
        for i in range(duration+1):
            dd = start + dt.timedelta(hours=i)
            dts.append(dd)

        return dts

    for dmanual, duracion in zip(manual.fechahora, manual.duracion):
        lst = create_dts(dmanual, duracion)
        for i in lst:
            auto = auto[auto.fechahora != i]
    auto.reset_index(inplace = True)
    autom = auto.iloc[:,1:]

    for dlost, duracion in zip(perdidos.fechahora, perdidos.duracion):
        lst = create_dts(dlost, duracion)
        for i in lst:
            auto = auto[auto.fechahora != i]
    auto.reset_index(inplace = True)
    autom = auto.iloc[:,1:]

    def get_flag(u, horas_ti):
        if u < len(horas_ti)- 1:
            if horas_ti[u] != 23:
                x = horas_ti[u+1] - horas_ti[u]
            elif horas_ti[u] == 23:
                x = horas_ti[u+1] - horas_ti[u] + 24
            flg = x==1
        else:
            flg = False
        return flg

    obs_data = pd.read_csv("outputs/observador_por_dia.csv")
    obs_d = pd.to_datetime(obs_data.fecha)
    obs_data["fecha_"] = [i.date() for i in obs_d]
    # recortando el df para hacer rápida la búsqueda
    def buscar_obser(fecha):
        m = obs_data[obs_data.fecha_ == fecha]
        obs = m.observador.to_list()[0]
        return obs

    p = autom.precip.to_list()
    dateti = autom.fechahora.to_list()
    horati = [i.hour for i in dateti]
    i = 0
    ## OBTENIENDO TODOS LOS EVENTOS QUE NO HAN SIDO REGISTRADOS
    # obtenemos solamente los indices inicial y final, luego recortaremos
    acum_lost = []; duraciones = []; hora_ini = []; observador_lost = []; n_flag = []
    while i <= len(p)-1:
        horaslst = [horati[i]]
        flaglst = [get_flag(i, horati)]
        flg = get_flag(i, horati)
        idx0 = i
        ac = p[i] #creado acumulado de la primera hora
        u = i
        while flg:
            u = u + 1
            ac = ac + p[u] # se suma a las horas de este evento
            horaslst.append(horati[u])
            flg = get_flag(u, horati)
            flaglst.append(flg)
            i = u
        idxf = u
        acum_lost.append(round(ac,1)) #acumulado sumado
        duraciones.append(idxf-idx0) #NOTA: Duración es horas después de la hora inicial
        hora_ini.append(dateti[idx0])
        f = dateti[idx0].date()
        o = buscar_obser(f)
        observador_lost.append(o)
        n_flag.append(2)
        i = u+1



    # ESTAS DOS COLUMNAS NOS SERVIRAN PARA COMPLETAR EL DATAFRAME
    fchs = [i.date() for i in hora_ini]
    pluv = np.zeros(len(fchs))

    df2 = pd.DataFrame(list(zip(fchs, hora_ini, duraciones, pluv, acum_lost, observador_lost, n_flag)), columns = ["fecha", "fechahora", "duracion", "pluvio", "precip", "observador", "tipo"])
    #print(df2.head())
    dflost = perdidos
    dflost["fecha"] = [i.date() for i in dflost.fechahora]
    dflost["pluvio"] = np.zeros(len(dflost.fecha))
    #print(dflost.head())
    dfmanual = manual.copy()
    dfmanual = dfmanual[["fecha", "fechahora", "pluvio", "conico","observador", "duracion", "tipo"]]
    dfmanual["precip"] = manual.acum
    
    dffinal = pd.concat([df2, dflost, dfmanual], axis = 0)
    dffinal.sort_values("fechahora", inplace = True)
    dffinal['conico'] = dffinal.conico.fillna(0)
    dffinal["duracion"] = dffinal.duracion + 1
    dffinal.to_csv("outputs/all_events.csv", index = False)

    return

if __name__ == "__main__":
    date_start  = "2023-01-01"            #fecha de inicio
    date_fin    = "2023-12-31"            #fecha de fin
    complete_table(date_start, date_fin)