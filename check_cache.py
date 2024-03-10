def check_cache(d0, df):
    from cache import date_start, date_fin
    if d0 != date_start and df != date_fin:
        print("Diferentes fechas, generando tablas de nuevo")
        f = open("cache.py", "w")
        f.write(f"date_start = '{d0}'")
        f.write(f"date_fin = '{df}'")
        f.close()
        flg = True
    else:
        print("Datos ya procesados, ignorando calculos")
        flg = False
    return flg
        