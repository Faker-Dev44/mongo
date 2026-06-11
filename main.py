from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import artists,artworks,catalog,categories

app = FastAPI(title="Atrium Catalog API")


#----Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  #React/Next.js si usan front
    "http://localhost:5000",  
    "*"                       
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Permite los orígenes de la lista
    allow_credentials=True,
    allow_methods=["*"],              # Permite todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],              # Permite todos los headers
)
#----Configuración de CORS



app.include_router(artists.router)
app.include_router(categories.router)
app.include_router(artworks.router)
app.include_router(catalog.router)

