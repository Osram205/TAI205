#1. importaciones
from fastapi import FastAPI, HTTPException, status, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic,HTTPBasicCredentials
import secrets


#2. Inicialización APP
app= FastAPI(
            title='Mi primer API',
            description='Osman Ramírez',
            version='1.0.0'
            )

# BD ficticia
usuarios=[
    {"id": 1, "nombre":"Osman Ramírez", "edad":21},
    {"id": 2, "nombre":"Benjamin Morales", "edad":20},
    {"id": 3, "nombre":"Yesenia Pintor", "edad":23},
]

#Modelo de Validaciones Pydantic
class crear_usuario(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de usuario")
    nombre:str = Field(...,min_length=3, max_length=50, example="Juanita")
    edad:int = Field(..., ge=1, le=123, description="Edad validad entre 1 y 123")

#Seguridad HTTPBasic
seguridad = HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials = Depends(seguridad)):
    userAuth= secrets.compare_digest(credenciales.username,"osmanram")
    passAuth= secrets.compare_digest(credenciales.password,"123456")

    if not(userAuth and passAuth):
        raise HTTPException (
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credencial no autorizada"
        )

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
async def eliminar_usuario(id:int, userAuth : str = Depends(verificar_peticion)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuario_eliminado = usuarios.pop(index)
            return {
                "message": f"Usuario eliminado correctamente por {userAuth}",
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")