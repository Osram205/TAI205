from fastapi import HTTPException, status, Depends,APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

routerU= APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)

@routerU.get("/")
async def consultaT(id:int):
    return{
        "status":"200",
        "total": len(usuarios),
        "data":usuarios
    }

@routerU.post("/")
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

@routerU.put("/{id}")
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

@routerU.delete("/{id}")
async def eliminar_usuario(id:int, userAuth : str = Depends(verificar_peticion)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index)
            return {
                "message": f"Usuario eliminado correctamente por {userAuth}",
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")