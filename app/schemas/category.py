from pydantic import BaseModel, Field

class CategoryBase(BaseModel):
    id_sql: int = Field(..., description="ID de la categoría en PostgreSQL")
    nombre_categoria: str = Field(..., description="Nombre del género o disciplina")
    detalles: dict[str, str] = Field(
        ..., 
        description="Mapeo de atributos y sus tipos de datos (Ej: {'duracion': 'Integer', 'fps': 'Decimal', 'resolucion': 'String', 'es_color': 'Boolean'})"
    )

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    pass