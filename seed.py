import asyncio
from datetime import datetime, timezone

from app.config.database import db

# ===================================================================
# COLECCIONES
# ===================================================================
COL_CATEGORIES = "categories"
COL_ARTISTS = "artists"
COL_ARTWORKS = "artworks"

# ===================================================================
# CATEGORÍAS (5)
# ===================================================================
CATEGORIES = [
    {
        "id_sql": 1,
        "detalles": ["tecnica", "soporte", "alto_cm", "ancho_cm"],
    },
    {
        "id_sql": 2,
        "detalles": ["material", "peso_kg", "largo_cm", "ancho_cm", "profundidad_cm"],
    },
    {
        "id_sql": 3,
        "detalles": ["tecnica", "papel", "alto_cm", "ancho_cm", "edicion"],
    },
    {
        "id_sql": 4,
        "detalles": ["tipo_arcilla", "tecnica_coccion", "peso_kg", "alto_cm", "ancho_cm", "profundidad_cm", "esmaltado"],
    },
    {
        "id_sql": 5,
        "detalles": ["material", "tecnica", "peso_g", "alto_cm", "ancho_cm", "profundidad_cm", "quilates"],
    },
]

# ===================================================================
# ARTISTAS (10)
# ===================================================================
ARTISTS = [
    {
        "id_sql": 1,
        "nombre": "Carlos",
        "apellido": "Mendoza",
        "fecha_nac": "1975-03-12",
        "fecha_fal": None,
        "nacionalidad": "Mexicana",
        "descripcion": "Pintor contemporáneo especializado en óleo y acrílico",
        "fotografia": "https://ejemplo.com/carlos_mendoza.jpg",
        "estado": "Activo",
    },
    {
        "id_sql": 2,
        "nombre": "Lucía",
        "apellido": "Fernández",
        "fecha_nac": "1982-07-25",
        "fecha_fal": None,
        "nacionalidad": "Argentina",
        "descripcion": "Acuarelista y artista gráfica",
        "fotografia": "https://ejemplo.com/lucia_fernandez.jpg",
        "estado": "Activo",
    },
    {
        "id_sql": 3,
        "nombre": "Antonio",
        "apellido": "Rivas",
        "fecha_nac": "1968-11-02",
        "fecha_fal": None,
        "nacionalidad": "Española",
        "descripcion": "Escultor en bronce y hierro forjado",
        "fotografia": "https://ejemplo.com/antonio_rivas.jpg",
        "estado": "Activo",
    },
    {
        "id_sql": 4,
        "nombre": "Sofía",
        "apellido": "Lombardi",
        "fecha_nac": "1970-05-18",
        "fecha_fal": None,
        "nacionalidad": "Italiana",
        "descripcion": "Escultora de mármol y piedra",
        "fotografia": "https://ejemplo.com/sofia_lombardi.jpg",
        "estado": "Activo",
    },
    {
        "id_sql": 5,
        "nombre": "Diego",
        "apellido": "Torres",
        "fecha_nac": "1990-09-30",
        "fecha_fal": None,
        "nacionalidad": "Colombiana",
        "descripcion": "Fotógrafo documental y de arte urbano",
        "fotografia": "https://ejemplo.com/diego_torres.jpg",
        "estado": "Activo",
    },
    {
        "id_sql": 6,
        "nombre": "Maya",
        "apellido": "Kusunoki",
        "fecha_nac": "1985-12-14",
        "fecha_fal": None,
        "nacionalidad": "Japonesa",
        "descripcion": "Fotógrafa de paisajes y minimalismo",
        "fotografia": "https://ejemplo.com/maya_kusunoki.jpg",
        "estado": "Activo",
    },
    {
        "id_sql": 7,
        "nombre": "Pedro",
        "apellido": "Huamán",
        "fecha_nac": "1965-04-08",
        "fecha_fal": None,
        "nacionalidad": "Peruana",
        "descripcion": "Ceramista especializado en gres y raku",
        "fotografia": "https://ejemplo.com/pedro_huaman.jpg",
        "estado": "Activo",
    },
    {
        "id_sql": 8,
        "nombre": "Yuki",
        "apellido": "Tanaka",
        "fecha_nac": "1978-01-22",
        "fecha_fal": None,
        "nacionalidad": "Japonesa",
        "descripcion": "Maestro ceramista en porcelana",
        "fotografia": "https://ejemplo.com/yuki_tanaka.jpg",
        "estado": "Activo",
    },
    {
        "id_sql": 9,
        "nombre": "Isabel",
        "apellido": "Cruz",
        "fecha_nac": "1988-06-05",
        "fecha_fal": None,
        "nacionalidad": "Puertorriqueña",
        "descripcion": "Orfebre contemporánea especializada en filigrana y fundición",
        "fotografia": "https://ejemplo.com/isabel_cruz.jpg",
        "estado": "Activo",
    },
    {
        "id_sql": 10,
        "nombre": "Hiroshi",
        "apellido": "Nakamura",
        "fecha_nac": "1972-10-19",
        "fecha_fal": None,
        "nacionalidad": "Japonesa",
        "descripcion": "Orfebre de lujo especializado en repujado y engaste",
        "fotografia": "https://ejemplo.com/hiroshi_nakamura.jpg",
        "estado": "Activo",
    },
]

# ===================================================================
# OBRAS (15 — 3 por cada género)
# ===================================================================
ARTWORKS = [
    # --- PINTURA (id_sql 1 — genero_id 1) ---
    {
        "id_sql": 1,
        "genero_id": 1,
        "autor_id": 1,
        "nombre": "El Sueño Dorado",
        "fecha_creacion": "2022-06-15",
        "precio_obra": 12500.00,
        "porcentaje_ganancia": 10.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/sueno_dorado.jpg",
        "detalles": {
            "tecnica": "óleo",
            "soporte": "lienzo",
            "alto_cm": "80",
            "ancho_cm": "60",
        },
    },
    {
        "id_sql": 2,
        "genero_id": 1,
        "autor_id": 1,
        "nombre": "Amanecer en el Valle",
        "fecha_creacion": "2023-03-10",
        "precio_obra": 8900.00,
        "porcentaje_ganancia": 8.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/amanecer_valle.jpg",
        "detalles": {
            "tecnica": "acrílico",
            "soporte": "lienzo",
            "alto_cm": "100",
            "ancho_cm": "70",
        },
    },
    {
        "id_sql": 3,
        "genero_id": 1,
        "autor_id": 2,
        "nombre": "Reflejos del Alma",
        "fecha_creacion": "2024-01-20",
        "precio_obra": 4500.00,
        "porcentaje_ganancia": 10.0,
        "estatus": "Reservada",
        "foto": "https://ejemplo.com/reflejos_alma.jpg",
        "detalles": {
            "tecnica": "acuarela",
            "soporte": "papel",
            "alto_cm": "56",
            "ancho_cm": "76",
        },
    },
    # --- ESCULTURA (id_sql 4-6 — genero_id 2) ---
    {
        "id_sql": 4,
        "genero_id": 2,
        "autor_id": 3,
        "nombre": "El Pensador Moderno",
        "fecha_creacion": "2021-11-05",
        "precio_obra": 35000.00,
        "porcentaje_ganancia": 10.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/pensador_moderno.jpg",
        "detalles": {
            "material": "bronce",
            "peso_kg": "120",
            "largo_cm": "90",
            "ancho_cm": "55",
            "profundidad_cm": "50",
        },
    },
    {
        "id_sql": 5,
        "genero_id": 2,
        "autor_id": 4,
        "nombre": "Eterna Armonía",
        "fecha_creacion": "2020-09-12",
        "precio_obra": 48000.00,
        "porcentaje_ganancia": 10.0,
        "estatus": "Vendida",
        "foto": "https://ejemplo.com/eterna_armonia.jpg",
        "detalles": {
            "material": "mármol",
            "peso_kg": "350",
            "largo_cm": "150",
            "ancho_cm": "60",
            "profundidad_cm": "60",
        },
    },
    {
        "id_sql": 6,
        "genero_id": 2,
        "autor_id": 3,
        "nombre": "Vuelo Libre",
        "fecha_creacion": "2023-07-03",
        "precio_obra": 18000.00,
        "porcentaje_ganancia": 8.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/vuelo_libre.jpg",
        "detalles": {
            "material": "hierro",
            "peso_kg": "85",
            "largo_cm": "110",
            "ancho_cm": "30",
            "profundidad_cm": "30",
        },
    },
    # --- FOTOGRAFÍA (id_sql 7-9 — genero_id 3) ---
    {
        "id_sql": 7,
        "genero_id": 3,
        "autor_id": 5,
        "nombre": "Silencio Urbano",
        "fecha_creacion": "2023-05-18",
        "precio_obra": 3200.00,
        "porcentaje_ganancia": 8.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/silencio_urbano.jpg",
        "detalles": {
            "tecnica": "digital",
            "papel": "Hahnemühle FineArt",
            "alto_cm": "60",
            "ancho_cm": "90",
            "edicion": "3",
        },
    },
    {
        "id_sql": 8,
        "genero_id": 3,
        "autor_id": 5,
        "nombre": "Raíces",
        "fecha_creacion": "2022-10-08",
        "precio_obra": 2800.00,
        "porcentaje_ganancia": 8.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/raices.jpg",
        "detalles": {
            "tecnica": "analógica",
            "papel": "",
            "alto_cm": "40",
            "ancho_cm": "50",
            "edicion": "5",
        },
    },
    {
        "id_sql": 9,
        "genero_id": 3,
        "autor_id": 6,
        "nombre": "Horizonte Infinito",
        "fecha_creacion": "2024-02-14",
        "precio_obra": 1500.00,
        "porcentaje_ganancia": 5.0,
        "estatus": "Reservada",
        "foto": "https://ejemplo.com/horizonte_infinito.jpg",
        "detalles": {
            "tecnica": "digital",
            "papel": "Canson Infinity",
            "alto_cm": "50",
            "ancho_cm": "75",
            "edicion": "",
        },
    },
    # --- CERÁMICA (id_sql 10-12 — genero_id 4) ---
    {
        "id_sql": 10,
        "genero_id": 4,
        "autor_id": 7,
        "nombre": "Vasija del Tiempo",
        "fecha_creacion": "2023-08-22",
        "precio_obra": 2200.00,
        "porcentaje_ganancia": 8.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/vasija_tiempo.jpg",
        "detalles": {
            "tipo_arcilla": "gres",
            "tecnica_coccion": "esmaltado",
            "peso_kg": "4.5",
            "alto_cm": "40",
            "ancho_cm": "25",
            "profundidad_cm": "25",
            "esmaltado": "true",
        },
    },
    {
        "id_sql": 11,
        "genero_id": 4,
        "autor_id": 8,
        "nombre": "Cuenco Lunar",
        "fecha_creacion": "2024-04-05",
        "precio_obra": 3800.00,
        "porcentaje_ganancia": 10.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/cuenco_lunar.jpg",
        "detalles": {
            "tipo_arcilla": "porcelana",
            "tecnica_coccion": "bizcocho",
            "peso_kg": "1.2",
            "alto_cm": "18",
            "ancho_cm": "30",
            "profundidad_cm": "30",
            "esmaltado": "false",
        },
    },
    {
        "id_sql": 12,
        "genero_id": 4,
        "autor_id": 7,
        "nombre": "El Abrazo",
        "fecha_creacion": "2021-12-01",
        "precio_obra": 1600.00,
        "porcentaje_ganancia": 5.0,
        "estatus": "Vendida",
        "foto": "https://ejemplo.com/abrazo_ceramica.jpg",
        "detalles": {
            "tipo_arcilla": "loza",
            "tecnica_coccion": "raku",
            "peso_kg": "2.8",
            "alto_cm": "35",
            "ancho_cm": "20",
            "profundidad_cm": "15",
            "esmaltado": "",
        },
    },
    # --- ORFEBRERÍA (id_sql 13-15 — genero_id 5) ---
    {
        "id_sql": 13,
        "genero_id": 5,
        "autor_id": 9,
        "nombre": "Collar Estelar",
        "fecha_creacion": "2023-11-30",
        "precio_obra": 9500.00,
        "porcentaje_ganancia": 10.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/collar_estelar.jpg",
        "detalles": {
            "material": "plata",
            "tecnica": "filigrana",
            "peso_g": "85",
            "alto_cm": "25",
            "ancho_cm": "8",
            "profundidad_cm": "0.5",
            "quilates": "",
        },
    },
    {
        "id_sql": 14,
        "genero_id": 5,
        "autor_id": 10,
        "nombre": "Anillo del Sol",
        "fecha_creacion": "2022-07-14",
        "precio_obra": 22000.00,
        "porcentaje_ganancia": 10.0,
        "estatus": "Reservada",
        "foto": "https://ejemplo.com/anillo_sol.jpg",
        "detalles": {
            "material": "oro",
            "tecnica": "repujado",
            "peso_g": "24",
            "alto_cm": "3",
            "ancho_cm": "2.5",
            "profundidad_cm": "2.5",
            "quilates": "18",
        },
    },
    {
        "id_sql": 15,
        "genero_id": 5,
        "autor_id": 9,
        "nombre": "Pulsera Eterna",
        "fecha_creacion": "2024-06-01",
        "precio_obra": 6800.00,
        "porcentaje_ganancia": 8.0,
        "estatus": "Disponible",
        "foto": "https://ejemplo.com/pulsera_eterna.jpg",
        "detalles": {
            "material": "bronce",
            "tecnica": "fundición",
            "peso_g": "55",
            "alto_cm": "6",
            "ancho_cm": "6",
            "profundidad_cm": "0.8",
            "quilates": "",
        },
    },
]


async def seed():
    print("=" * 50)
    print("  SEED — Atrium Catalog")
    print("=" * 50)

    # ── Categorías ────────────────────────────────────────────────
    print("\n[CATEGORÍAS] Insertando...")
    for cat in CATEGORIES:
        existing = await db[COL_CATEGORIES].find_one({"id_sql": cat["id_sql"]})
        if existing:
            print(f"   [SKIP] id_sql={cat['id_sql']} ya existe")
            continue
        await db[COL_CATEGORIES].insert_one(cat)
        print(f"   [OK] id_sql={cat['id_sql']} insertada")

    # ── Artistas ──────────────────────────────────────────────────
    print("\n[ARTISTAS] Insertando...")
    for art in ARTISTS:
        existing = await db[COL_ARTISTS].find_one({"id_sql": art["id_sql"]})
        if existing:
            print(f"   [SKIP] id_sql={art['id_sql']} — {art['nombre']} {art['apellido']} ya existe")
            continue
        await db[COL_ARTISTS].insert_one(art)
        print(f"   [OK] id_sql={art['id_sql']} — {art['nombre']} {art['apellido']}")

    # ── Obras ─────────────────────────────────────────────────────
    print("\n[OBRAS] Insertando...")
    for obra in ARTWORKS:
        existing = await db[COL_ARTWORKS].find_one({"id_sql": obra["id_sql"]})
        if existing:
            print(f"   [SKIP] id_sql={obra['id_sql']} — '{obra['nombre']}' ya existe")
            continue
        await db[COL_ARTWORKS].insert_one(obra)
        print(f"   [OK] id_sql={obra['id_sql']} — '{obra['nombre']}'")

    # ── Resumen ───────────────────────────────────────────────────
    print("\n" + "=" * 50)
    print("  [COMPLETADO] Seed finalizado exitosamente")
    print(f"     Categorías: {len(CATEGORIES)}")
    print(f"     Artistas:   {len(ARTISTS)}")
    print(f"     Obras:      {len(ARTWORKS)}")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(seed())
