from pydantic import BaseModel, Field
from typing import Optional

class ArtistBase(BaseModel):
    id_sql: int = Field(..., description="ID del artista en SQL (id)")
    nombre: str = Field(..., max_length=100)
    apellido: str = Field(..., max_length=100)
    fecha_nac: Optional[str] = Field(None, description="fechaNac")
    fecha_fal: Optional[str] = Field(None, description="fechaFal")
    nacionalidad: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    fotografia: Optional[str] = Field(None, max_length=255)
    estado: str = Field("Activo", description="Activo o Inactivo")

class ArtistCreate(ArtistBase):
    pass

class ArtistResponse(ArtistBase):
    pass