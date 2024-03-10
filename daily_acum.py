def daily_acum(date_start, date_fin):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import datetime as dt
    m = pd.read_csv("outputs/processed.csv")
    a = pd.read_csv("data/automatico.csv")


    # Obteniendo los datos del automatico que no fueron registrados, primero quitando
    # los datos
    def create_dts(start, duration):
        dts = []
        for i in range(duration+1):
            dd = start + dt.timedelta(hours=i)
            dts.append(dd)

        return dts

    m["fechahora"] = pd.to_datetime(m.fechahora)
    a["fechahora"] = pd.to_datetime(a.fechahora)
    start_daily = 7 # HORA DESDE LA QUE SE CUENTA UN DIA

    # Recortando ambas tablas
    d0 = dt.datetime.strptime(date_start, "%Y-%m-%d")
    df = dt.datetime.strptime(date_fin, "%Y-%m-%d")
    m = m.loc[(m.fechahora > d0) & (m.fechahora < df)]
    a = a.loc[(a.fechahora > d0) & (a.fechahora < df)]
    a.reset_index(inplace = True)
    a = a.iloc[:,1:]

    horas = [i.hour for i in m.fechahora]
    fechas = []
    for f, h, d in zip(m.fechahora, horas, m.duracion):
        hh = np.arange(int(h), int(h) + int(d) +1)
        if 7 in hh:
            if np.median(hh) < 7.5:
                #entonces se le asocia al dia antes
                #print(hh, np.median(hh), "antes")
                fechas.append(f)
            elif np.median(hh) > 7.5:
                #entonces se le asocia al dia despues
                #print(hh, np.median(hh), "despues")  
                fechas.append(f + dt.timedelta(days = 1))
            elif np.median(hh) == 7.5:
                #print(hh, np.median(hh), "caos")
                fechas.append(f) #por ahora se le asocia al dia anteior 
        elif hh[0] > 7:
            fechas.append(f + dt.timedelta(days = 1))
        else:
            fechas.append(f)

    dia = [i.date() for i in fechas]
    df2 = pd.DataFrame(list(zip(m.fechahora,dia,m.pluvio)), columns = ["fecha","dia","manual"])
    df2 = df2.groupby("dia").sum()
    df2.reset_index(inplace=True)
    df2["dia"] = pd.to_datetime(df2.dia)
    #df2.to_csv("prueba.csv")


    ## PROCESAMIENTO AUTOMATICO
    #print(a.head())
    horas = [i.hour for i in a.fechahora]
    nfechas = []
    for f, h in zip(a.fechahora, horas):
        if h <= 7:
            nfechas.append(f)
        else:
            nfechas.append(f + dt.timedelta(days = 1))
    dias = [i.date() for i in nfechas]

    df3 = pd.DataFrame(list(zip(a.fechahora, dias, a.precip)), columns = ["fecha", "dia", "automatico"])
    df3 = df3.groupby("dia").sum()
    df3.reset_index(inplace=True)
    df3["dia"] = pd.to_datetime(df3.dia)

    dff = df2.merge(df3, how = "right", on = "dia")
    dff["manual"] = dff.manual.fillna(0)

    obs = pd.read_csv("outputs/observador_por_dia.csv")
    obs = obs[["fecha","observador"]]
    obs.columns = ["dia", "observador"]
    obs["dia"] = pd.to_datetime(obs.dia)

    dff2 = dff.merge(obs, how = "left", on="dia")
    dff2.to_csv("outputs/daily_acum.csv", index = False)
    return