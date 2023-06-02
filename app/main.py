from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.staticfiles import StaticFiles
from funciones.buscar_enfermedades import buscar_enfermedades
from funciones.obtener_examenes import obtener_examenes
from funciones.obtener_tipo_riesgo import obtener_tipo_riesgo




app = FastAPI()
templates = Jinja2Templates(directory="src")
static_directory = "static"  # Ruta a la carpeta static de tu proyecto
static_files = StaticFiles(directory=static_directory)

app.mount("/static", static_files, name="static")


# Configuracion CORS
origins = ["*"]  # Agrega los orígenes permitidos aquí

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/enfermedades")
def obtener_enfermedades(request: Request):
    # Leer los datos del archivo XLSX con pandas
    df = pd.read_excel("data/baseDeDatosEnfermedades.xlsx", usecols=[0], header=0)
    enfermedades = df.iloc[:, 0].tolist()
    # Devolver las opciones de enfermedades como respuesta JSON
    return {"enfermedades": enfermedades}

@app.get("/tipos_cirugia")
def obtener_tipos_cirugia(request: Request):
    # Leer los datos del archivo XLSX con pandas
    df = pd.read_excel("data/BaseDeDatosCirugias.xlsx", header=None)
    tipos_cirugia = df[0].tolist()
    # Eliminar la primera opción que corresponde a la cabecera
    tipos_cirugia = tipos_cirugia[1:]
    # Devolver los tipos de cirugía como opciones
    return {"tipos_cirugia": tipos_cirugia}


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/formulario")
async def mostrar_formulario(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

@app.post("/analisis_paciente", response_class=HTMLResponse)
async def analisis_paciente(request: Request):
    # Cargar el dataframe de Enfermedades desde el archivo Excel
    df_enfermedades = pd.read_excel("data/EnfermedadesAsa.xlsx")
    df_enfermedades.columns = df_enfermedades.columns.str.strip()
    form_data = await request.form()
    edad = int(form_data.get("edad", 0))
    tipo_cirugia = form_data.get("tipo_cirugia", "")
    enfermedades_adyacentes = form_data.getlist("enfermedad_adyacente[]")
    
    
    # Obtener los tipos de ASA correspondientes a las enfermedades adyacentes
    tipo_asa = buscar_enfermedades(enfermedades_adyacentes)
    

    # Obtener el tipo de riesgo de la cirugía correspondiente al tipo de ASA encontrado
    tipo_riesgo = obtener_tipo_riesgo(tipo_cirugia)

    # Obtener el primer tipo de ASA de la lista
    examenes = obtener_examenes(tipo_asa, tipo_riesgo)

    # Crear el objeto JSON de respuesta
    respuesta = {
        "edad": edad,
        "asa": tipo_asa,
        "tipo_riesgo": tipo_riesgo,
        "examenes": examenes
    }

    html_content = templates.TemplateResponse("respuesta.html", {"request": request, "respuesta": respuesta})

    return html_content






   



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)





    
##enfermedad: Individuo saludable sin enfermedades.
##cirugia: Histerectomía abdominal