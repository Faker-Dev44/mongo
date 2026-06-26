from fastapi import APIRouter, HTTPException, status
from app.config.database import db
from app.schemas.artwork import ArtworkCreate, ArtworkResponse
import re

router = APIRouter(prefix="/artwork", tags=["Artworks"])

@router.post("/", response_model=ArtworkResponse)
async def create_artwork(artwork: ArtworkCreate):
    # 1. Validar existencia del artista
    artista = await db.artists.find_one({"id_sql": artwork.autor_id})
    if not artista:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El artista con ID {artwork.autor_id} no existe en MongoDB."
        )

    # 2. Validar existencia de la categoría
    categoria = await db.categories.find_one({"id_sql": artwork.genero_id})
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El género con ID {artwork.genero_id} no existe en MongoDB."
        )
    
    # 3. Validar y tipar los atributos polimórficos de la obra de forma dinámica
    definicion_atributos = categoria.get("detalles", {})
    
    for campo_esperado, tipo_esperado in definicion_atributos.items():
        if campo_esperado not in artwork.detalles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Falta el atributo técnico requerido: '{campo_esperado}'"
            )
            
        valor_recibido = artwork.detalles[campo_esperado].strip()
        
        # Validar tipo de dato
        if tipo_esperado == "Integer":
            if not re.match(r"^-?\d+$", valor_recibido):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El campo '{campo_esperado}' debe ser un número entero válido."
                )
        elif tipo_esperado == "Decimal":
            if not re.match(r"^-?\d+(\.\d+)?$", valor_recibido):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El campo '{campo_esperado}' debe ser un número decimal válido."
                )
        elif tipo_esperado == "Boolean":
            if valor_recibido.lower() not in ["true", "false", "1", "0", "sí", "no"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El campo '{campo_esperado}' debe ser un booleano (true/false)."
                )
        # Si es 'String', se acepta cualquier valor de texto

    # 4. Inserción del documento
    await db.artworks.insert_one(artwork.model_dump())
    return artwork

@router.get("/", response_model=list[ArtworkResponse])
async def read_artwork_all():
    cursor = db.artworks.find()
    return await cursor.to_list(length=1000)

@router.get("/{id}", response_model=ArtworkResponse | dict)
async def read_artwork_id(id: int):
    artwork = await db.artworks.find_one({"id_sql": id})
    if not artwork:
        return {"error": "Obra no encontrada."}
    return artwork

@router.put("/{id}")
async def update_artwork_id(id: int, artwork: ArtworkCreate):
    artista = await db.artists.find_one({"id_sql": artwork.autor_id})
    categoria = await db.categories.find_one({"id_sql": artwork.genero_id})
    if not artista or not categoria:
        return {"error": "Actualización rechazada. 'autor_id' o 'genero_id' inválidos."}

    await db.artworks.update_one({"id_sql": id}, {"$set": artwork.model_dump()})
    return {"msg": "Obra actualizada", "id_sql": id}

@router.delete("/{id}")
async def delete_artwork_id(id: int):
    await db.artworks.delete_one({"id_sql": id})
    return {"msg": "Obra eliminada", "id_sql": id}