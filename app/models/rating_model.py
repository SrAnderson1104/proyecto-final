"""
MODELO de calificaciones (funcionalidad opcional).

Guarda las calificaciones de 1 a 5 en la tabla Calificacion y calcula el promedio.
"""

import sqlite3
from datetime import date

from app.database import get_connection
from app.errors import DatabaseError


def create_rating(movie_id, person, score):
    """Guarda una calificación nueva con la fecha de hoy y devuelve la calificación creada."""
    today = date.today().isoformat()

    query = """
        INSERT INTO Calificacion (id_pelicula, persona, calificacion, fecha)
        VALUES (?, ?, ?, ?)
    """

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (movie_id, person, score, today))
        connection.commit()
        new_id = cursor.lastrowid
        connection.close()
    except sqlite3.Error:
        raise DatabaseError("No se ha podido guardar la calificación")

    return {
        "id": new_id,
        "id_pelicula": movie_id,
        "persona": person,
        "calificacion": score,
        "fecha": today,
    }


def get_rating_summary(movie_id):
    """
    Devuelve el promedio de calificaciones de una película y cuántas tiene.
    Si no tiene ninguna, el promedio es 0.
    """
    query = """
        SELECT AVG(calificacion) AS promedio, COUNT(*) AS total
        FROM Calificacion
        WHERE id_pelicula = ?
    """

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (movie_id,))
        row = cursor.fetchone()
        connection.close()
    except sqlite3.Error:
        raise DatabaseError("No se han podido leer las calificaciones")

    total = row["total"]

    # AVG devuelve None cuando no hay filas
    if row["promedio"] is None:
        average = 0
    else:
        average = round(row["promedio"], 1)

    return {
        "id_pelicula": movie_id,
        "promedio": average,
        "total": total,
    }
