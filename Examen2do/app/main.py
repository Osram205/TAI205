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

reservas_list=[
    {"id":1, "huesped":"Carlos", "fecha_e":"10/02/23", "fecha_s":"13/02/23", "tipo_habitacion":"sencilla", "confirmar_reserva":1},
    {"id":2, "huesped":"Maria", "fecha_e":"10/02/24", "fecha_s":"13/02/24", "tipo_habitacion":"doble","confirmar_reserva":0},
    {"id":3, "huesped":"Marisol", "fecha_e":"10/02/25", "fecha_s":"13/02/25", "tipo_habitacion":"suite","confirmar_reserva":1},
]

class crear_reserva(BaseModel):
    id:int=Field(...,gt=0, description="Identificador Reserva")
    huesped:str=Field(..., min_length=5, max_length=50,example="Jesus")
    fecha_e:str=Field(..., example="20/12/2023", description="La fecha no puede ser menor al dia de hoy")
    fecha_s:str=Field(...,example="20/10/2023", description="La estancia no puede ser mayor a 7 días, la fecha no puede ser menor a la fecha de entrada")
    tipo_habitacion:str=Field(..., examples=["Sencilla","Doble","Suite"])

class confirmar_reserva(BaseModel):  
    id:int=Field(...,gt=0, description="Identificador Reserva")
    huesped:str=Field(..., min_length=5, max_length=50,example="Jesus")
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
async def consultaR(id:int):
    return{
        "status":"200",
        "total": len(reservas_list),
        "data":reservas_list
    }

@app.post("/reserva/{id}", tags=['CRUD HTTP'])
async def crear_reserva(reserva:crear_reserva, userAuth: str = Depends(verificar_peticion)):
    for rsv in reservas_list:
        if rsv ["id"] == reservas_list.id:
            raise HTTPException(status_code=400,detail="El id ya existe")
    reserva.append(reservas_list)
    return{
        "mensaje":"reserva agregada correctamente",
        "status":"200",
        "reserva":reservas_list
        }

@app.put("/reserva/{id}", tags=['CRUD HTTP'])
async def confirmar_reserva(reserva:confirmar_reserva):
    for index, rsv in enumerate(reservas_list):
        if rsv["id"] == id:
            reservas_list[index].update(reserva)
            return {
                "mensaje": "Reserva actualizada correctamente",
                "status": "200",
                "usuario": reservas_list[index]
            }
    raise HTTPException(status_code=400, detail="Reserva no encontrada")

