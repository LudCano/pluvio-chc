
## CODIGO DE ENCONTRAR EVENTOS PERDIDOS
## ---------------------------------------


def lost_events(date_start, date_fin, do_plot):
    # Librerias
    import pandas as pd
    import datetime as dt
    import numpy as np
    import matplotlib.pyplot as plt
    ## ---------------------------------------

    #########################################
    ###########   PROCESANDO   ##############
    #########################################
    manual_path = "data/manual.csv"       #ruta a archivo procesado pluvio manual
    auto_path   = "data/automatico.csv"   #ruta a archivo procesado pluvio automatico


    # Leyendo archivos
    manual = pd.read_csv(manual_path)
    automatico = pd.read_csv(auto_path)
    manual["fechahora"] = pd.to_datetime(manual.fechahora)
    automatico["fechahora"] = pd.to_datetime(automatico.fechahora)
    ## ---------------------------------------


    # Recortando ambas tablas
    d0 = dt.datetime.strptime(date_start, "%Y-%m-%d")
    df = dt.datetime.strptime(date_fin, "%Y-%m-%d")
    manual = manual.loc[(manual.fechahora > d0) & (manual.fechahora < df)]
    automatico = automatico.loc[(automatico.fechahora > d0) & (automatico.fechahora < df)]
    automatico.reset_index(inplace = True)
    automatico = automatico.iloc[:,1:]

    # Obteniendo los datos del automatico que no fueron registrados, primero quitando
    # los datos
    def create_dts(start, duration):
        dts = []
        for i in range(duration+1):
            dd = start + dt.timedelta(hours=i)
            dts.append(dd)

        return dts

    def get_flag(u, horas_ti):
        if horas_ti[u] != 23:
            x = horas_ti[u+1] - horas_ti[u]
        elif horas_ti[u] == 23:
            x = horas_ti[u+1] - horas_ti[u] + 24
        flg = x==1
        return flg



    obs_data = pd.read_csv("outputs/observador_por_dia.csv")
    obs_d = pd.to_datetime(obs_data.fecha)
    obs_data["fecha_"] = [i.date() for i in obs_d]
    # recortando el df para hacer rápida la búsqueda
    def buscar_obser(fecha):
        m = obs_data[obs_data.fecha_ == fecha]
        obs = m.observador.to_list()[0]
        return obs

    autom = automatico.copy()
        
    for dmanual, duracion in zip(manual.fechahora, manual.duracion):
        lst = create_dts(dmanual, duracion)
        for i in lst:
            autom = autom[autom.fechahora != i]
        
    autom.reset_index(inplace = True)
    autom = autom.iloc[:,1:]
    autom.to_csv("prueba.csv")
    #print(autom.head())
    p = autom.precip.to_list()
    dateti = autom.fechahora.to_list()
    horati = [i.hour for i in dateti]
    i = 0
    ## OBTENIENDO INDICES DE EVENTOS QUE TIENEN PRECIP >0
    # obtenemos solamente los indices inicial y final, luego recortaremos
    acum_lost = []; duraciones = []; hora_ini = []; observador_lost = []; n_flag = []
    while i <= len(p)-1:
        if p[i] > 0:
            horaslst = [horati[i]]
            flaglst = [get_flag(i, horati)]
            flg = get_flag(i, horati)
            idx0 = i
            ac = p[i] #creado acumulado de la primera hora
            u = i
            while (p[u+1] != 0) and (flg):
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
            n_flag.append(1)
            f = dateti[idx0].date()
            o = buscar_obser(f)
            observador_lost.append(o)
            i = u+1
        else:
            i = i+1

    df2 = pd.DataFrame(list(zip(hora_ini, duraciones, acum_lost, observador_lost, n_flag)), columns = ["fechahora", "duracion", "precip", "observador", "tipo"])
    df2.to_csv("outputs/eventos_perdidos.csv", index = False)
    if do_plot:
        bns = np.arange(min(duraciones), max(duraciones)+1, 1)
        fig, ax = plt.subplots(1,1)
        ax.hist(duraciones, bins = bns)
        ax.set_title("Duracioń de eventos perdidos")
        ax.set_xlabel("Duracion [h]")
        ax.set_ylabel("Número de eventos perdidos")
        fig.savefig("outputs/histo_duracion.png", dpi = 300)

        fig2, ax2 = plt.subplots(1,1)
        ax2.scatter(duraciones, acum_lost)
        ax2.set_title("Duracioń y acumulado de eventos perdidos")
        ax2.set_xlabel("Duracion [h]")
        ax2.set_ylabel("Acumulado en el evento perdido [mm]")
        fig2.savefig("outputs/duracion_acumulado.png", dpi = 300)


        horas_lost = [i.hour for i in hora_ini]
        fig, ax = plt.subplots(1,1)
        ax.hist(horas_lost, bins = 24)
        ax.set_title("Horas del día de eventos perdidos")
        ax.set_xlabel("Hora del día")
        ax.set_ylabel("Número de eventos perdidos")
        fig.savefig("outputs/histo_horadia.png", dpi = 300)

        fig, ax = plt.subplots(1,1)
        ax.scatter(horas_lost, duraciones)
        ax.set_title("Horas del día de eventos perdidos")
        ax.set_xlabel("Hora del día")
        ax.set_ylabel("Duración del evento perdido (horas)")
        fig.savefig("outputs/duracion_hora.png", dpi = 300)

    return


if __name__ == "__main__":
    ## PARAMETROS EJECUCION
    date_start  = "2023-01-01"            #fecha de inicio
    date_fin    = "2023-12-31"            #fecha de fin
    threshold   = 1                       #cantidad de eventos para tomar en cuenta un observador
    ## ---------------------------------------