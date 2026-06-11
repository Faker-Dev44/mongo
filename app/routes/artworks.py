from fastapi import APIRouter
from app.config.database import db
from app.schemas.artwork import ArtworkCreate, ArtworkResponse

router = APIRouter(prefix="/artwork", tags=["Artworks"])

# Endpoint - Create (Con doble validación cruzada: Artista y Género NoSQL)
@router.post("/", response_model=ArtworkResponse | dict)
async def create_artwork(artwork: ArtworkCreate):
    # 1. Validar si el Autor/Artista existe en la colección 'artists' dev MongoDB
    artista = await db.artists.find_one({"id_sql": artwork.autor_id})
    if not artista:
        return {"error": f"El artista con ID {artwork.autor_id} no existe en el catálogo NoSQL. No se puede crear la obra."}

    # 2. Buscar el Género/Categoría usando el genero_id de la obra
    categoria = await db.categories.find_one({"id_sql": artwork.genero_id})
    if not categoria:
        return {"error": f"El género con ID {artwork.genero_id} no existe."}
    
    # 3. Validar la estructura polimórfica (Requisitos específicos de las subtablas)
    requisitos = categoria.get("detalles", [])
    for campo_obligatorio in requisitos:
        if campo_obligatorio not in artwork.detalles:
            return {
                "error": "Validación de estructura NoSQL fallida",
                "detalle": f"Para guardar este género, el diccionario 'detalles' debe incluir obligatoriamente el campo '{campo_obligatorio}'"
            }
            
    # 4. Guardar con éxito en MongoDB Atlas
    await db.artworks.insert_one(artwork.model_dump())
    return artwork

# Endpoint - Get All
@router.get("/", response_model=list[ArtworkResponse])
async def read_artwork_all():
    cursor = db.artworks.find()
    artworks_db = await cursor.to_list(length=100)
    return artworks_db

# Endpoint - Get por ID SQL
@router.get("/{id}", response_model=ArtworkResponse | dict)
async def read_artwork_id(id: int):
    artwork = await db.artworks.find_one({"id_sql": id})
    if not artwork:
        return {"error": f"Obra con ID {id} no encontrada."}
    return artwork

# Endpoint - Update
@router.put("/{id}")
async def update_artwork_id(id: int, artwork: ArtworkCreate):
    # Primero verificamos si el autor o género nuevos son válidos antes de actualizar
    artista = await db.artists.find_one({"id_sql": artwork.autor_id})
    categoria = await db.categories.find_one({"id_sql": artwork.genero_id})
    
    if not artista or not categoria:
        return {"error": "Actualización rechazada. 'autor_id' o 'genero_id' inválidos."}

    await db.artworks.update_one({"id_sql": id}, {"$set": artwork.model_dump()})
    return {"msg": "Obra actualizada correctamente", "id_sql": id}

# Endpoint - Delete
@router.delete("/{id}")
async def delete_artwork_id(id: int):
    await db.artworks.delete_one({"id_sql": id})
    return {"msg": "Obra borrada del catálogo", "id_sql": id}
