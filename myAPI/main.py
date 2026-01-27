#1. importaciones
from fastapi import FastAPI

#2. Inicialización APP
app= FastAPI()

#3. Endpoints
@app.get("/")
async def holaMundo():
    return {"mensaje":"Hola Mundo FASTAPI"}

@app.get("/bienvenidos")
async def holaMundo():
    return {"mensaje":"Bienvenidos"}
