"""
MODELO de comentarios.

Guarda y lee los comentarios de la tabla Comentario de SQLite.
"""

import sqlite3
from datetime import date

from app.database import get_connection
from app.errors import DatabaseError


def row_to_dict(row):
    """Convierte una fila de SQLite en un diccionario normal de Python."""
    return {
        "id": row["id"],
        "id_pelicula": row["id_pelicula"],
        "persona": row["persona"],
        "comentario": row["comentario"],
        "fecha": row["fecha"],
    }


def get_comments_by_movie(movie_id):
    """Devuelve todos los comentarios de una película, del más reciente al más antiguo."""
    query = """
        SELECT id, id_pelicula, persona, comentario, fecha
        FROM Comentario
        WHERE id_pelicula = ?
        ORDER BY id DESC
    """

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (movie_id,))
        rows = cursor.fetchall()
        connection.close()
    except sqlite3.Error:
        raise DatabaseError("No se han podido leer los comentarios")

    comments = []
    for row in rows:
        comments.append(row_to_dict(row))

    return comments


def create_comment(movie_id, person, text):
    """Guarda un comentario nuevo con la fecha de hoy y devuelve el comentario creado."""
    today = date.today().isoformat()  # Ejemplo: "2026-10-25"

    query = """
        INSERT INTO Comentario (id_pelicula, persona, comentario, fecha)
        VALUES (?, ?, ?, ?)
    """

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (movie_id, person, text, today))
        connection.commit()
        new_id = cursor.lastrowid
        connection.close()
    except sqlite3.Error:
        raise DatabaseError("No se ha podido guardar el comentario")

    return {
        "id": new_id,
        "id_pelicula": movie_id,
        "persona": person,
        "comentario": text,
        "fecha": today,
    }
