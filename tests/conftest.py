"""
Preparación común para todos los tests.

- Usamos una base de datos SQLite temporal para no tocar la real.
- Sustituimos las llamadas a OMDb por respuestas falsas (así los tests
  no dependen de Internet ni de la API key).
"""

import pytest
from fastapi.testclient import TestClient

import config
from app.models import movie_model


# Respuesta falsa de OMDb para una búsqueda
FAKE_SEARCH_RESPONSE = {
    "Response": "True",
    "Search": [
        {"imdbID": "tt0133093", "Title": "The Matrix", "Year": "1999", "Type": "movie", "Poster": "N/A"},
        {"imdbID": "tt0234215", "Title": "The Matrix Reloaded", "Year": "2003", "Type": "movie", "Poster": "N/A"},
    ],
}

# Respuesta falsa de OMDb cuando no encuentra nada
FAKE_NOT_FOUND_RESPONSE = {"Response": "False", "Error": "Movie not found!"}

# Respuesta falsa de OMDb para un detalle
FAKE_DETAIL_RESPONSE = {
    "Response": "True",
    "Title": "The Matrix",
    "Year": "1999",
    "Runtime": "136 min",
    "Genre": "Action, Sci-Fi",
    "Director": "Lana Wachowski, Lilly Wachowski",
    "Actors": "Keanu Reeves, Laurence Fishburne",
    "Plot": "Un programador descubre la verdad sobre su realidad.",
    "Poster": "N/A",
    "imdbRating": "8.7",
}


def fake_call_omdb(params):
    """Imita a OMDb: devuelve una respuesta falsa según los parámetros que recibe."""
    # Búsqueda (parámetro "s")
    if "s" in params:
        if params["s"] == "matrix":
            return FAKE_SEARCH_RESPONSE
        return FAKE_NOT_FOUND_RESPONSE

    # Detalle (parámetro "i")
    if "i" in params:
        if params["i"] == "tt0133093":
            return FAKE_DETAIL_RESPONSE
        return FAKE_NOT_FOUND_RESPONSE

    return FAKE_NOT_FOUND_RESPONSE


@pytest.fixture
def client(tmp_path, monkeypatch):
    """
    Crea un cliente de pruebas con:
    - base de datos temporal (se borra sola al terminar el test)
    - OMDb falso
    """
    # 1. Base de datos temporal
    temp_db_path = tmp_path / "test.db"
    monkeypatch.setattr(config, "DATABASE_PATH", str(temp_db_path))

    # 2. OMDb falso
    monkeypatch.setattr(movie_model, "call_omdb", fake_call_omdb)

    # 3. Creamos la aplicación (esto también crea las tablas en la base de datos temporal)
    from main import create_app
    app = create_app()

    return TestClient(app)
