from pydantic import BaseModel,Field
#Importante utilizar solo esas importaciones para realizar los Schemas
#De aqui para abajo, se deben realizar los 'Schemas'
#Para cosas opcionales utilizar el operador: '|' que significa 'O'

#Importante utilizar solo esas importaciones para realizar los Schemas
#De aqui para abajo, se deben realizar los 'Schemas'
#Para cosas opcionales utilizar el operador: '|' que significa 'O'

#ArtworkBase
#Lo que se definira aqui es: 
# id_sql - Tipo entero 
# id_category - Tipo entero
# detalles - Tipo lista dict/diccionarios

#ArtworkCreate
#Este 'scheme' heredara simplemente de 'ArtworkBase'

#ArtworkResponse
#Este 'scheme' heredara simplemente de 'ArtworkBase'


from pydantic import BaseModel, Field
from typing import Optional

class ArtworkBase(BaseModel):
    id_sql: int = Field(..., description="ID de la obra en SQL (id)")
    genero_id: int = Field(..., description="ID del género/categoría (genero_id)")
    autor_id: int = Field(..., description="ID del artista/autor (autor_id)")
    nombre: str = Field(..., max_length=150, description="Nombre de la obra")
    fecha_creacion: Optional[str] = Field(None, description="Fecha de creación (fechaCreacion)")
    precio_obra: float = Field(..., description="Precio base (precioObra)")
    porcentaje_ganancia: Optional[float] = Field(None, description="Entre 5 y 10 por ciento")
    estatus: str = Field("Disponible", description="Valores: Disponible, Reservada, Vendida")
    foto: Optional[str] = Field(None, description="Ruta de la imagen de la obra")
    
    # NUESTRO SELLO POLIMÓRFICO: Aquí mueren las 5 tablas extras de SQL
    detalles: dict[str, str] = Field(..., description="Diccionario con campos dinámicos (Ej: tecnica, peso, tipoEsmalte)")

class ArtworkCreate(ArtworkBase):
    pass

class ArtworkResponse(ArtworkBase):
    pass