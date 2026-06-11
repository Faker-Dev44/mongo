from fastapi import APIRouter
from app.config.database import db
from app.schemas.artist import ArtistCreate, ArtistResponse

router = APIRouter(prefix="/artist", tags=["Artists"])

# Endpoint - Create Artista
@router.post("/", response_model=ArtistResponse | dict)
async def create_artist(artist: ArtistCreate):
    # Validar que no se duplique el id_sql
    existe = await db.artists.find_one({"id_sql": artist.id_sql})
    if existe:
        return {"error": f"El artista con ID {artist.id_sql} ya está registrado."}
        
    await db.artists.insert_one(artist.model_dump())
    return artist

# Endpoint - Get All Artistas
@router.get("/", response_model=list[ArtistResponse])
async def read_artist_all():
    cursor = db.artists.find()
    artists_db = await cursor.to_list(length=100)
    return artists_db

# Endpoint - Get Artista por ID SQL
@router.get("/{id}", response_model=ArtistResponse | dict)
async def read_artist_id(id: int):
    artist = await db.artists.find_one({"id_sql": id})
    if not artist:
        return {"error": f"Artista con ID {id} no encontrado."}
    return artist

# Endpoint - Update Artista
@router.put("/{id}")
async def update_artist_id(id: int, artist: ArtistCreate):
    resultado = await db.artists.update_one({"id_sql": id}, {"$set": artist.model_dump()})
    if resultado.matched_count == 0:
        return {"error": f"No se encontró ningún artista con ID {id} para actualizar."}
    return {"msg": "Artista actualizado con éxito", "id_sql": id}

# Endpoint - Delete Artista
@router.delete("/{id}")
async def delete_artist_id(id: int):
    # Ojo Middleware: Antes de borrar un artista, podrías verificar si tiene obras asociadas
    obras_asociadas = await db.artworks.find_one({"autor_id": id})
    if obras_asociadas:
        return {"error": f"No se puede borrar el artista {id} porque tiene obras registradas en el catálogo."}

    await db.artists.delete_one({"id_sql": id})
    return {"msg": "Artista eliminado del catálogo NoSQL", "id_sql": id}