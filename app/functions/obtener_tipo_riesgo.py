import pandas as pd

def obtener_tipo_riesgo(tipo_cirugia):
    # Cargar el dataframe de Tipos de Cirugías desde el archivo Excel
    df_cirugias = pd.read_excel("data/ListaDeCirugias.xlsx")
    df_cirugias.columns = df_cirugias.columns.str.strip()

    if tipo_cirugia in df_cirugias["Bajo Riesgo"].values:
        return "Bajo Riesgo"
    elif tipo_cirugia in df_cirugias["Riesgo Medio"].values:
        return "Riesgo Medio"
    elif tipo_cirugia in df_cirugias["Alto Riesgo"].values:
        return "Alto Riesgo"
    else:
        return "Sin clasificar"  # Valor por defecto si no se cumple ninguna condición
