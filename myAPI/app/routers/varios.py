from fastapi import APIRouter
import asyncio
from typing import Optional

routerV= APIRouter(
    tags=['Inicio']
)

#3. Endpoints
@routerV.get("/")
async def holaMundo():
    return {"mensaje":"Hola Mundo FASTAPI"}

@routerV.get("/v1/bienvenidos")
async def bien():
    return {"mensaje":"Bienvenidos"}

@routerV.get("/v1/promedio")
async def promedio():
    await asyncio.sleep(3)
    return {
            "Calificación":"7",
            "Estatus":"200"
            }

@routerV.get("/v1/parametroO/{id}")
async def consultaUno(id:int):
    await asyncio.sleep(3)
    return {
            "Resultado":"Usuario Encontrado",
            "Estatus":"200"
            }