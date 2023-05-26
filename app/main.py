from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="src")

# Configuracion CORS
origins = ["*"]  # Agrega los orígenes permitidos aquí

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

@app.get("/formulario")
async def mostrar_formulario(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

# Definir la ruta y el método HTTP para el endpoint
@app.post("/analisis_paciente", response_class=HTMLResponse)
async def analisis_paciente(request: Request):
    # Cargar el dataframe de Enfermedades desde el archivo Excel
    df_enfermedades = pd.read_excel("data/EnfermedadesAsa.xlsx")
    df_enfermedades.columns = df_enfermedades.columns.str.strip()
    form_data = await request.form()
    edad = int(form_data["edad"])
    tipo_cirugia = form_data["tipo_cirugia"]
    enfermedad_adyacente = form_data["enfermedad_adyacente"]
    

    # Función para buscar la enfermedad en las columnas y determinar el tipo de ASA correspondiente
    def buscar_enfermedad(row):
        if enfermedad_adyacente == row["ASA 1"]:
            return "ASA 1"
        elif enfermedad_adyacente == row["ASA 2"]:
            return "ASA 2"
        elif enfermedad_adyacente == row["ASA 3"]:
            return "ASA 3"
        elif enfermedad_adyacente == row["ASA 4"]:
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
    tipo_riesgo = obtener_tipo_riesgo(tipo_cirugia)

    if tipo_riesgo is not None:
        examenes = obtener_examenes(tipo_asa, tipo_riesgo)

    # Crear el objeto JSON de respuesta
    respuesta = {"edad": edad, "asa": tipo_asa, "tipo_riesgo": tipo_riesgo, "examenes": examenes}
    
    html_content = templates.TemplateResponse("respuesta.html", {"request": request, "respuesta": respuesta})

    return html_content

   



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)




    
##enfermedad: Individuo saludable sin enfermedades.
##cirugia: Histerectomía abdominal