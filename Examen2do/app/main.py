from fastapi import FastAPI, HTTPException, status, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic,HTTPBasicCredentials
import secrets

app=FastAPI (        
        title='Examen2do',
        description= 'Osman Ramírez',
        version='1.0.0'
        )

reservas=[
    {"id":1, "huesped":"Carlos", "fecha_e":"10/02/23", "fecha_s":"13/02/23", "tipo_habitacion":"sencilla", "confirmar_reserva":1},
    {"id":2, "huesped":"Maria", "fecha_e":"10/02/24", "fecha_s":"13/02/24", "tipo_habitacion":"doble","confirmar_reserva":0},
    {"id":3, "huesped":"Marisol", "fecha_e":"10/02/25", "fecha_s":"13/02/25", "tipo_habitacion":"suite","confirmar_reserva":1},
]

class crear_reserva(BaseModel):
    id:int=Field(...,gt=0, description="Identificador Reserva")
    huesped:str=Field(..., min_length=5, max_length=50,example="Jesus")
    fecha_e:str=Field(...)
    fecha_s:str=Field(...)
    tipo_habitacion:str=Field(...)
    confirmar_reserva:int=Field(..., ge=0,le=1, description= "1 para confirmar, 0 para pendiente")

seguridad = HTTPBasic()

def verificar_peticion(credenciales:HTTPBasicCredentials = Depends(seguridad)):
    userAuth= secrets.compare_digest(credenciales.username,"hotel")
    passAuth= secrets.compare_digest(credenciales.password,"r2026")

    if not(userAuth and passAuth):
        raise HTTPException (
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Credencial no autorizada"
        )


@app.get("/reserva/{id}}", tags=['CRUD HTTP'])
async def reservas_list(id:int):
    return{
        "status":"200",
        "total": len(reservas),
        "data":reservas
    }