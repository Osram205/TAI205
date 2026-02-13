#1. importaciones
from fastapi import FastAPI, HTTPException
from typing import Optional
import asyncio

#2. Inicialización APP
app= FastAPI(
            title='Mi primer API',
            description='Osman Ramírez',
            version='1.0.0'
            )

# BD ficticia
usuarios=[
    {"id":"1", "nombre":"Osman Ramírez", "edad":"21"},
    {"id":"2", "nombre":"Benjamin Morales", "edad":"20"},
    {"id":"3", "nombre":"Yesenia Pintor", "edad":"23"},
]


#3. Endpoints
@app.get("/", tags=['Inicio'])
async def holaMundo():
    return {"mensaje":"Hola Mundo FASTAPI"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bien():
    return {"mensaje":"Bienvenidos"}

@app.get("/v1/promedio", tags=['Promedio'])
async def promedio():
    await asyncio.sleep(3)
    return {
            "Calificación":"7",
            "Estatus":"200"
            }

@app.get("/v1/parametroO/{id}", tags=['Parametros'])
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {
            "Resultado":"Usuario Encontrado",
            "Estatus":"200"
            }

@app.get("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def consultaT(id:int):
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }

@app.post("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def crear_usuario(usuario:dict):
    for usr in usuarios:
        if usr ["id"] == usuario.get("id"):
            raise HTTPException(status_code=400,detail="El id ya existe")
    usuarios.append(usuario)
    return{
        "mensaje":"usuario agregado correctamente",
        "status":"200",
        "usuario":usuario
        }