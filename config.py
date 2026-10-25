"""
Configuración del proyecto.

Aquí guardamos los valores que usa toda la aplicación (API key, URL de OMDb,
ruta de la base de datos...). La API key NO se escribe en el código: se lee
del fichero .env para que no acabe subida al repositorio.
"""

import os

# Carpeta donde está este fichero (la raíz del proyecto)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ruta del fichero .env con nuestras claves
ENV_FILE_PATH = os.path.join(BASE_DIR, ".env")


def load_env_file(file_path):
    """Lee el fichero .env línea a línea y guarda cada valor como variable de entorno."""
    # Si no existe el fichero .env, no hacemos nada
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()

            # Saltamos las líneas vacías y los comentarios
            if line == "" or line.startswith("#"):
                continue

            # Saltamos las líneas que no tienen el formato CLAVE=valor
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


# Cargamos el .env nada más importar este fichero
load_env_file(ENV_FILE_PATH)

# ---------- API externa OMDb ----------
OMDB_URL = "https://www.omdbapi.com/"
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")

# Segundos máximos que esperamos a que OMDb responda
REQUEST_TIMEOUT = 10

# ---------- Base de datos SQLite ----------
DATABASE_PATH = os.getenv("DATABASE_PATH", os.path.join(BASE_DIR, "peliculas.db"))

# ---------- Vistas (front-end) ----------
VIEWS_DIR = os.path.join(BASE_DIR, "views")
