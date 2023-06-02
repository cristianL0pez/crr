import pandas as pd
def buscar_enfermedades(enfermedades_adyacentes):
    # Cargar el dataframe de Enfermedades desde el archivo Excel
    df_enfermedades = pd.read_excel("data/EnfermedadesAsa.xlsx")
    df_enfermedades.columns = df_enfermedades.columns.str.strip()

    tipos_asa = []

    for enfermedad in enfermedades_adyacentes:
        for col in df_enfermedades.columns:
            if enfermedad in df_enfermedades[col].values:
                tipos_asa.append((enfermedad, col))

    tipos_asa = sorted(list(set(tipos_asa)), key=lambda x: x[1], reverse=True)

    return tipos_asa




