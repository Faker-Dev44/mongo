from pydantic import BaseModel,Field
#Importante utilizar solo esas importaciones para realizar los Schemas
#De aqui para abajo, se deben realizar los 'Schemas'
#Para cosas opcionales utilizar el operador: '|' que significa 'O'

#CategoryBase
#Lo que se definira aqui es: 
# id_sql - Tipo entero 
# detalles - Tipo lista de string (list[str])

#CategoryCreate
#Este 'scheme' heredara simplemente de 'CategoryBase'

#CategoryResponse
#Este 'scheme' heredara simplemente de 'CategoryBase'


class CategoryBase(BaseModel):
    """
    Schema base que define la estructura común para las categorías de arte.
    Mapea las plantillas dinámicas en MongoDB asociadas al ID de la base relacional.
    """
    id_sql: int = Field(
        ..., 
        description="Identificador único correlativo de la categoría proveniente de la base de datos de Node.js"
    )
    detalles: list[str] = Field(
        ..., 
        description="Lista de strings que define la plantilla de campos dinámicos para este género artístico"
    )

class CategoryCreate(CategoryBase):
    """
    Schema utilizado para la creación o registro de nuevas categorías en el microservicio.
    Hereda directamente de CategoryBase.
    """
    pass

class CategoryResponse(CategoryBase):
    """
    Schema utilizado para estructurar las respuestas de las categorías devueltas por la API.
    Hereda directamente de CategoryBase.
    """
    pass


