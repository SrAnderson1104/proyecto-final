"""
Tests de películas: búsqueda, detalle y control de errores.
"""

from app.errors import InvalidDataError
from app.models.movie_model import imdb_id_to_number, number_to_imdb_id


# ---------- Conversión de ids ----------

def test_imdb_id_to_number():
    assert imdb_id_to_number("tt0133093") == 133093


def test_number_to_imdb_id():
    assert number_to_imdb_id(133093) == "tt0133093"


def test_imdb_id_invalid_raises_error():
    try:
        imdb_id_to_number("abc")
        assert False, "Debería haber lanzado InvalidDataError"
    except InvalidDataError:
        pass


# ---------- Búsqueda ----------

def test_search_by_title_returns_movies(client):
    response = client.get("/api/peliculas/buscar?titulo=matrix")

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["peliculas"][0]["titulo"] == "The Matrix"
    assert data["peliculas"][0]["id_pelicula"] == 133093


def test_search_by_title_and_year(client):
    response = client.get("/api/peliculas/buscar?titulo=matrix&anio=1999")

    assert response.status_code == 200
    assert response.json()["total"] == 2


def test_search_not_found_returns_empty_list(client):
    response = client.get("/api/peliculas/buscar?titulo=pelicula-que-no-existe")

    assert response.status_code == 200
    assert response.json()["total"] == 0
    assert response.json()["peliculas"] == []


def test_search_without_title_returns_400(client):
    response = client.get("/api/peliculas/buscar?titulo=&anio=1999")

    assert response.status_code == 400
    assert "título" in response.json()["detail"]


def test_search_with_bad_year_returns_400(client):
    response = client.get("/api/peliculas/buscar?titulo=matrix&anio=99")

    assert response.status_code == 400
    assert "año" in response.json()["detail"]


# ---------- Detalle ----------

def test_movie_detail_returns_data(client):
    response = client.get("/api/peliculas/133093")

    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "The Matrix"
    assert data["director"] == "Lana Wachowski, Lilly Wachowski"
    assert data["id_pelicula"] == 133093


def test_movie_detail_not_found_returns_404(client):
    response = client.get("/api/peliculas/999999")

    assert response.status_code == 404


def test_movie_detail_with_text_id_returns_422(client):
    response = client.get("/api/peliculas/abc")

    assert response.status_code == 422


# ---------- Vistas ----------

def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Buscar película" in response.text


def test_detail_page_loads(client):
    response = client.get("/pelicula/133093")

    assert response.status_code == 200
    assert "Comentarios" in response.text


def test_favicon_loads(client):
    response = client.get("/favicon.ico")

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/svg+xml"
