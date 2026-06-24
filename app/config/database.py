import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("ERROR: La variable de entorno MONGO_URI no está configurada")

# Conectar al cliente
client = AsyncIOMotorClient(MONGO_URI)

#
# SOLUCIÓN: Forzar el nombre de la base de datos directamente
db = client["atrium_db_ej"]