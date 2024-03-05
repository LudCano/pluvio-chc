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