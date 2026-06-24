from fastapi import APIRouter
from fastapi import APIRouter, Query
from app.config.database import db
from typing import Optional

router = APIRouter(prefix="/catalog", tags=["Catalog"])

# Reemplazar el endpoint search_catalog en app/routes/catalog.py:

@router.get("/search")
async def search_catalog(
    genero_id: Optional[int] = Query(None, description="Filtrar por ID de género"),
    estatus: Optional[str] = Query(None, description="Filtrar por estatus"),
    precio_max: Optional[float] = Query(None, description="Precio máximo"),
    page: int = Query(1, ge=1, description="Número de página de la consulta"),
    limit: int = Query(12, ge=1, le=100, description="Cantidad de registros por página")
):
    pipeline = []

    # 1. Filtros dinámicos ($match)
    match_stage = {}
    if genero_id is not None:
        match_stage["genero_id"] = genero_id
    if estatus is not None:
        match_stage["estatus"] = estatus
    if precio_max is not None:
        match_stage["precio_obra"] = {"$lte": precio_max}

    if match_stage:
        pipeline.append({"$match": match_stage})

    # 2. OPTIMIZACIÓN DE PAGINACIÓN NO BLOQUEANTE (Antes del $lookup para ahorrar I/O)
    skip_amount = (page - 1) * limit
    pipeline.append({"$skip": skip_amount})
    pipeline.append({"$limit": limit})

    # 3. ETAPA DE LECTURA DE RELACIÓN ($lookup)
    pipeline.append({
        "$lookup": {
            "from": "artists",
            "localField": "autor_id",
            "foreignField": "id_sql",
            "as": "informacion_artista"
        }
    })

    pipeline.append({
        "$unwind": {
            "path": "$informacion_artista",
            "preserveNullAndEmptyArrays": True
        }
    })

    cursor = db.artworks.aggregate(pipeline)
    resultados = await cursor.to_list(length=limit)

    for doc in resultados:
        doc["_id"] = str(doc["_id"])
        if "informacion_artista" in doc and doc["informacion_artista"]:
            doc["informacion_artista"]["_id"] = str(doc["informacion_artista"]["_id"])

    return resultados