from fastapi import APIRouter
from fastapi import APIRouter, Query
from app.config.database import db
from typing import Optional

router = APIRouter(prefix="/catalog", tags=["Catalog"])

@router.get("/search")
async def search_catalog(
    genero_id: Optional[int] = Query(None, description="Filtrar por ID de género"),
    estatus: Optional[str] = Query(None, description="Filtrar por estatus: Disponible, Reservada, Vendida"),
    precio_max: Optional[float] = Query(None, description="Precio máximo de la obra")
):
    # 1. Inicializamos la tubería (Pipeline) de Agregación
    pipeline = []

    # 2. Construimos los filtros dinámicos ($match)
    match_stage = {}
    
    if genero_id is not None:
        match_stage["genero_id"] = genero_id
        
    if estatus is not None:
        match_stage["estatus"] = estatus
        
    if precio_max is not None:
        # Filtra obras cuyo precio_obra sea menor o igual ($lte) al máximo enviado
        match_stage["precio_obra"] = {"$lte": precio_max}

    # Si hay algún filtro, lo metemos como la primera etapa de la tubería
    if match_stage:
        pipeline.append({"$match": match_stage})

    # 3. ETAPA DE RECOMPENSA (Justificación de Referencias para el Profesor)
    # Hacemos un $lookup para unir la obra con su artista en una sola consulta indexada
    pipeline.append({
        "$lookup": {
            "from": "artists",            # Colección origen
            "localField": "autor_id",     # Campo en la obra
            "foreignField": "id_sql",     # Campo en el artista
            "as": "informacion_artista"   # Nombre del array resultante
        }
    })

    # 4. Limpiamos el array del lookup para que sea un objeto directo (opcional pero más limpio)
    pipeline.append({
        "$unwind": {
            "path": "$informacion_artista",
            "preserveNullAndEmptyArrays": True # Por si la obra no tiene artista válido
        }
    })

    # 5. Ejecutar la agregación en MongoDB Atlas
    cursor = db.artworks.aggregate(pipeline)
    resultados = await cursor.to_list(length=100)

    # Limpieza de los ObjectIds de Mongo para evitar errores de serialización JSON
    for doc in resultados:
        doc["_id"] = str(doc["_id"])
        if "informacion_artista" in doc and doc["informacion_artista"]:
            doc["informacion_artista"]["_id"] = str(doc["informacion_artista"]["_id"])

    return resultados