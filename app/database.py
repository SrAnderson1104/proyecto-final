"""
Conexión con la base de datos SQLite y creación de las tablas.
"""

import sqlite3

import config
from app.errors import DatabaseError

# Tabla de comentarios (columnas tal y como pide el enunciado)
CREATE_COMMENT_TABLE = """
CREATE TABLE IF NOT EXISTS Comentario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pelicula INTEGER NOT NULL,
    persona TEXT NOT NULL,
    comentario TEXT NOT NULL,
    fecha DATE NOT NULL
)
"""

# Tabla de calificaciones (funcionalidad opcional del enunciado)
CREATE_RATING_TABLE = """
CREATE TABLE IF NOT EXISTS Calificacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pelicula INTEGER NOT NULL,
    persona TEXT NOT NULL,
    calificacion INTEGER NOT NULL CHECK (calificacion BETWEEN 1 AND 5),
    fecha DATE NOT NULL
)
"""


def get_connection():
    """Abre una conexión con la base de datos."""
    connection = sqlite3.connect(config.DATABASE_PATH)

    # Con esto podemos leer cada fila como un diccionario: fila["persona"]
    connection.row_factory = sqlite3.Row

    return connection


def create_tables():
    """Crea las tablas si todavía no existen."""
    try:
        connection = get_connection()
    except sqlite3.Error:
        raise DatabaseError("No se ha podido abrir la base de datos")

    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_COMMENT_TABLE)
        cursor.execute(CREATE_RATING_TABLE)
        connection.commit()
    except sqlite3.Error:
        raise DatabaseError("No se han podido crear las tablas")
    finally:
        # El bloque finally se ejecuta siempre, haya error o no
        connection.close()
