from fastapi import APIRouter
from app.config.database import db
from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/category",tags=["Categories"])

#Coloca de aqui para abajo todos los endpoints pero con 'router' en vez de 'app'
#Hacer CRUD de enpoints para 'Categories' verificar correspondencia con  los schemas expuestos en 'Schemas/artwork.py'

#Enpoint - Create

#Enpoint - Update

#Enpoint - Get

#Enpoint - Delete

#===================


# Endpoint - Create
@router.post("/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate):
    # Inserta directamente el diccionario de los datos en MongoDB
    await db.categories.insert_one(category.model_dump())
    return category

# Endpoint - Get All (Listar todas)
@router.get("/", response_model=list[CategoryResponse])
async def read_category_all():
    cursor = db.categories.find()
    # Convierte el cursor de Mongo a una lista plana de Python
    categories_db = await cursor.to_list(length=100)
    return categories_db

# Endpoint - Get por ID (Buscar una)
@router.get("/{id}")
async def read_category_id(id: int):
    # Busca por el identificador numérico de SQL
    category = await db.categories.find_one({"id_sql": id})
    
    if category:
        category["_id"] = str(category["_id"])  # Limpieza obligatoria del ObjectId de Mongo
    return category

# Endpoint - Update
@router.put("/{id}")
async def update_category_id(id: int, category: CategoryCreate):
    # Modifica los campos usando el operador $set de MongoDB
    await db.categories.update_one({"id_sql": id}, {"$set": category.model_dump()})
    return {"msg": "Categoría actualizada", "id_sql": id}

# Endpoint - Delete
@router.delete("/{id}")
async def delete_category_id(id: int):
    # Remueve el documento que coincida con el id_sql
    await db.categories.delete_one({"id_sql": id})
    return {"msg": "Categoría borrada", "id_sql": id}
