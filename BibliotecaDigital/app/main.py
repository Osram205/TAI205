#importaciones
from fastapi import FastAPI, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel, Field

#inicialisacion app
app= FastAPI(
            title='Biblioteca Digital',
            description='Osman Ramírez',
            version='1.0.0'
            )
#3. Endpoints
@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bien():
    return {"mensaje":"Bienvenidos"}

