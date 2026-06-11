from pydantic import BaseModel,Field
#Importante utilizar solo esas importaciones para realizar los Schemas
#De aqui para abajo, se deben realizar los 'Schemas'
#Para cosas opcionales utilizar el operador: '|' que significa 'O'

class CategoryBase(BaseModel):
    id_sql: int = Field(..., description="ID de la categoría en SQL")
    detalles: list[str] = Field(..., description="Lista de detalles requeridos para esta categoría")

#CategoryCreate
#Este 'scheme' heredara simplemente de 'CategoryBase'
class CategoryCreate(CategoryBase):
    pass

#CategoryResponse
#Este 'scheme' heredara simplemente de 'CategoryBase'
class CategoryResponse(CategoryBase):
    pass


