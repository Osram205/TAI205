#1. importaciones
from fastapi import FastAPI, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel, Field


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

#Modelo de Validaciones Pydantic
class crear_usuario(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de usuario")
    nombre:str = Field(...,min_length=3, max_length=50, example="Juanita")
    edad:int = Field(..., ge=1, le=123, description="Edad validad entre 1 y 123")

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
async def crear_usuario(usuario:crear_usuario):
    for usr in usuarios:
        if usr ["id"] == usuario.id:
            raise HTTPException(status_code=400,detail="El id ya existe")
    usuarios.append(usuario)
    return{
        "mensaje":"usuario agregado correctamente",
        "status":"200",
        "usuario":usuario
        }

@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: str, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index].update(usuario_actualizado)
            return {
                "mensaje": "Usuario actualizado correctamente",
                "status": "200",
                "usuario": usuarios[index]
            }
    raise HTTPException(status_code=400, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: str):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(index)
            return {
                "mensaje": "Usuario eliminado correctamente",
                "status": "200",
                "usuario_eliminado": usuario_eliminado
            }
    raise HTTPException(status_code=400, detail="Usuario no encontrado")