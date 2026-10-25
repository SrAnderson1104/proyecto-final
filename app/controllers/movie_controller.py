"""
CONTROLADOR de películas.

Recibe las peticiones HTTP relacionadas con películas, llama al modelo
y devuelve la respuesta. Las rutas empiezan por /api/peliculas.
"""

from fastapi import APIRouter

from app.errors import InvalidDataError
from app.models import movie_model

router = APIRouter(prefix="/api/peliculas", tags=["Películas"])


def validate_search_params(title, year):
    """
    Comprueba que el título no está vacío (OMDb siempre lo exige)
    y que el año, si viene, tiene 4 dígitos.
    """
    if title == "":
        raise InvalidDataError("Debes indicar un título para buscar")

    if year != "":
        if not year.isdigit() or len(year) != 4:
            raise InvalidDataError("El año debe tener 4 dígitos, por ejemplo 1999")


@router.get("/buscar")
def search_movies(titulo: str = "", anio: str = ""):
    """
    Busca películas por título y, opcionalmente, por año.
    Ejemplos:
        /api/peliculas/buscar?titulo=matrix
        /api/peliculas/buscar?titulo=matrix&anio=1999
    """
    title = titulo.strip()
    year = anio.strip()

    validate_search_params(title, year)

    # Si no hay año lo pasamos como None para que el modelo lo ignore
    if year == "":
        year = None

    movies = movie_model.search_movies(title, year)

    return {"total": len(movies), "peliculas": movies}


@router.get("/{movie_id}")
def get_movie_detail(movie_id: int):
    """
    Devuelve el detalle de una película.
    Ejemplo: /api/peliculas/133093
    """
    movie = movie_model.get_movie_detail(movie_id)

    return movie
