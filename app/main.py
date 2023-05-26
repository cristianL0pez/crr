from typing import Union
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

# Configuracion CORS
origins = ["http://127.0.0.1", "http://127.0.0.1:5500", "http://127.0.0.1:80"]  # Agrega los orígenes permitidos aquí

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DatosPaciente(BaseModel):
    edad: int
    tipo_cirugia: str
    enfermedad_adyacente: str

@app.get("/tipos_cirugia")
async def obtener_tipos_cirugia():
    # Leer los datos del archivo XLSX con pandas
    df = pd.read_excel("data/BaseDeDatosCirugias.xlsx", usecols=[2], header=1)
    tipos_cirugia = df["Tipo de Cirugia"].tolist()
    # Devolver los tipos de cirugía como opciones
    return {"tipos_cirugia": tipos_cirugia}



# Definir la ruta y el método HTTP para el endpoint
@app.post("/analisis_paciente")
async def analisis_paciente(enfermedad_buscar: str, cirugia: str):
    # Cargar el dataframe de Enfermedades desde el archivo Excel
    df_enfermedades = pd.read_excel("data/EnfermedadesAsa.xlsx")
    df_enfermedades.columns = df_enfermedades.columns.str.strip()

    # Función para buscar la enfermedad en las columnas y determinar el tipo de ASA correspondiente
    def buscar_enfermedad(row):
        if enfermedad_buscar == row["ASA 1"]:
            return "ASA 1"
        elif enfermedad_buscar == row["ASA 2"]:
            return "ASA 2"
        elif enfermedad_buscar == row["ASA 3"]:
            return "ASA 3"
        elif enfermedad_buscar == row["ASA 4"]:
            return "ASA 4"
        else:
            return "No se encontró"

    # Aplicar la función a cada fila del dataframe y obtener el tipo de ASA correspondiente
    df_enfermedades["Tipo_ASA"] = df_enfermedades.apply(buscar_enfermedad, axis=1)

    # Obtener el tipo de ASA correspondiente a la enfermedad buscada
    tipo_asa = df_enfermedades.loc[df_enfermedades["Tipo_ASA"] != "No se encontró", "Tipo_ASA"].iloc[0]

    # Cargar el dataframe de Tipos de Cirugías desde el archivo Excel
    df_cirugias = pd.read_excel("data/ListaDeCirugias.xlsx")
    df_cirugias.columns = df_cirugias.columns.str.strip()
    
    
    
    def obtener_tipo_riesgo(cirugia):
        if cirugia in df_cirugias["Bajo Riesgo"].values:
            return "Bajo Riesgo"
        elif cirugia in df_cirugias["Riesgo Medio"].values:
            return "Riesgo Medio"
        elif cirugia in df_cirugias["Alto Riesgo"].values:
            return "Alto Riesgo"
        else:
            return None 

    def obtener_examenes(tipo_asa, tipo_riesgo):
        examenes = []

        if tipo_asa == "ASA 1":
            if tipo_riesgo == "Bajo Riesgo":
                examenes = ["No de rutina"]
            elif tipo_riesgo == "Riesgo Medio":
                examenes = ["No de rutina"]
            elif tipo_riesgo == "Alto Riesgo":
                examenes = ["Hemograma - Coagulación - ECG"]

        elif tipo_asa == "ASA 2":
            if tipo_riesgo == "Bajo Riesgo":
                examenes = ["No de rutina"]
            elif tipo_riesgo == "Riesgo Medio":
                examenes = ["Función renal - ECG"]
            elif tipo_riesgo == "Alto Riesgo":
                examenes = ["Hemograma - Coagulación - Función renal - ECG"]

        elif tipo_asa == "ASA 3":
            if tipo_riesgo == "Bajo Riesgo":
                examenes = ["Hemograma - Coagulación - ECG"]
            elif tipo_riesgo == "Riesgo Medio":
                examenes = ["Hemograma - Coagulación - Función renal - ECG"]
            elif tipo_riesgo == "Alto Riesgo":
                examenes = ["Hemograma - Coagulación - Función renal - ECG"]

        elif tipo_asa == "ASA 4":
            if tipo_riesgo == "Bajo Riesgo":
                examenes = ["Hemograma - Coagulación - ECG - Función renal"]
            elif tipo_riesgo == "Riesgo Medio":
                examenes = ["Hemograma - Coagulación - ECG - Función renal"]
            elif tipo_riesgo == "Alto Riesgo":
                examenes = ["Hemograma - Coagulación - ECG - Función renal"]

        return examenes

# Obtener el tipo de riesgo de la cirugía correspondiente al tipo de ASA encontrado
    tipo_riesgo = obtener_tipo_riesgo(cirugia)

    if tipo_riesgo is not None:
        examenes = obtener_examenes(tipo_asa, tipo_riesgo)

# Crear el objeto JSON de respuesta
    respuesta = {"asa": tipo_asa, "tipo_riesgo": tipo_riesgo, "examenes": examenes}

    return respuesta


    